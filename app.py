import os
from dotenv import load_dotenv
import streamlit as st
from cassandra.cluster import Cluster
from cassandra.io.asyncioreactor import AsyncioConnection
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import Cassandra
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
import tempfile

load_dotenv()

DOCKER_HOST_IP = os.getenv("DOCKER_HOST_IP")
OLLAMA_BASE_URL = f"http://{os.getenv('OLLAMA_HOST', '127.0.0.1')}:11434"
CASSANDRA_KEYSPACE = "rag_demo"
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "granite3.2:2b") #Set OLLAMA_MODEL from environment or default to "granite3.2:2b"

st.set_page_config(page_title="Yaoundé AI - Success Cluster", layout="wide")
st.title("Démonstration du TALLA RAG")


@st.cache_resource
def init_rag():
    try:
        cluster = Cluster(
            [DOCKER_HOST_IP], port=9042, connection_class=AsyncioConnection
        )
        session = cluster.connect(CASSANDRA_KEYSPACE)
    except Exception as e:
        st.error(f"❌ Could not connect to Cassandra at {DOCKER_HOST_IP}: {e}")
        return None

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text:v1.5", base_url=OLLAMA_BASE_URL
    )
    llm = ChatOllama(model="granite3.2:2b", base_url=OLLAMA_BASE_URL)

    vector_store = Cassandra(
        embedding=embeddings,
        session=session,
        keyspace=CASSANDRA_KEYSPACE,
        table_name="rag_vector_table",
    )
    return vector_store, llm


rag_tools = init_rag()

# --- SIDEBAR ---
with st.sidebar:
    st.header("Settings & Ingestion")
    if rag_tools:
        st.success(f"Connected to Cluster at {DOCKER_HOST_IP}")
    else:
        st.error("Cluster Offline")

    uploaded_file = st.file_uploader("Upload a file for the AI", type=["txt", "pdf"])
    if uploaded_file and st.button("Ingest to Cluster"):
        if rag_tools:
            vector_store, _ = rag_tools
            if uploaded_file.type == "application/pdf":
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name
                chunks = PyPDFLoader(tmp_path).load_and_split()
            else:
                raw_text = uploaded_file.read().decode("utf-8")
                text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
                chunks = text_splitter.create_documents([raw_text])
            with st.spinner("Replicating data across nodes..."):
                vector_store.add_documents(chunks)
            st.success(f"Ingested {len(chunks)} chunks successfully!")

    # Clear database button at bottom of sidebar
    if st.button("🗑️ Clear All Knowledge", type="primary", use_container_width=True):
        if rag_tools:
            vector_store, _ = rag_tools
            vector_store.session.execute("TRUNCATE rag_vector_table")
            st.success("Database wiped clean!")

# --- CHAT ---
if rag_tools:
    vector_store, llm = rag_tools

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question about your documents..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.status("Searching Cassandra Nodes...", expanded=False):
                results = vector_store.similarity_search(prompt, k=3)
                context = "\n".join([d.page_content for d in results])
                pages = [d.metadata.get("page") for d in results if "page" in d.metadata]
                if pages:
                    st.caption(f"📄 Sources — pages: {pages}")
            
            pre_prompt =  """
            Your name is "TALLA". You entire purpose is to help people have responses to their inquiries based on the provided context only.
            Provide clear, concise answers based on the context. If the answer is not in the documentation, state that you do not know and politely invite the user to provide context in the sense of their question.
            You are a friendly support agent. Use warm, conversational language, including contractions. Acknowledge the user's frustration and provide reassuring, helpful answers.
            You responses should be in the language of the user prompt. For example, You respond in French if prompt is in French or in English if prompt is in English and so on.

            - Assume the sender needs explanation about the context.
            - Prefer obvious explanations over lengthy over complicated ones.
            - Ask a follow-up question only when the issue is genuinely unclear.
            
            """

            full_prompt = (
                f"Context:\n{context}\n\nQuestion: {prompt}\n\n{pre_prompt}"
            )
            response = llm.invoke(full_prompt)
            st.markdown(response.content)
            st.session_state.messages.append(
                {"role": "assistant", "content": response.content}
            )
