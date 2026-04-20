import os
from dotenv import load_dotenv
from cassandra.cluster import Cluster
from cassandra.io.asyncioreactor import AsyncioConnection
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import Cassandra
from langchain_text_splitters import CharacterTextSplitter

load_dotenv()

CASSANDRA_IP = os.getenv("DOCKER_HOST_IP")
OLLAMA_BASE_URL = f"http://{os.getenv('OLLAMA_HOST', '127.0.0.1')}:11434"
CASSANDRA_KEYSPACE = "rag_demo"
EMBEDDING_MODEL = "nomic-embed-text:v1.5"
LLM_MODEL = "gemma3:12b"


class RAGManager:
    def __init__(self):
        self.cluster = Cluster(
            [CASSANDRA_IP], port=9042, connection_class=AsyncioConnection
        )
        self.session = self.cluster.connect(CASSANDRA_KEYSPACE)

        self.embeddings = OllamaEmbeddings(
            model=EMBEDDING_MODEL, base_url=OLLAMA_BASE_URL
        )
        self.llm = ChatOllama(model=LLM_MODEL, base_url=OLLAMA_BASE_URL)

        self.vector_store = Cassandra(
            embedding=self.embeddings,
            session=self.session,
            keyspace=CASSANDRA_KEYSPACE,
            table_name="rag_vector_table",
        )

    def ingest_document(self, text_content: str):
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = text_splitter.create_documents([text_content])
        self.vector_store.add_documents(docs)
        print(f"Ingested {len(docs)} chunks into Cassandra.")

    def query(self, question: str) -> str:
        relevant_docs = self.vector_store.similarity_search(question, k=3)
        context = "\n".join([doc.page_content for doc in relevant_docs])
        prompt = (
            f"Answer the question based ONLY on the following context:\n{context}\n\n"
            f"Question: {question}"
        )
        return self.llm.invoke(prompt).content


if __name__ == "__main__":
    rag = RAGManager()
    sample_text = (
        "The success_cluster consists of two nodes running on PC1. "
        "It uses Cassandra 5.0.6 for data replication."
    )
    rag.ingest_document(sample_text)
    ans = rag.query("How many nodes are in the success_cluster?")
    print(f"\nAI Response: {ans}")
