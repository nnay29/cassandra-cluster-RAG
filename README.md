

<!-- PROJECT LOGO -->
<br />
<div align="center" id="#readme-top">
  <a href="https://github.com/nnay29/cassandra-cluster-RAG">
    <img src="images/taximan-talla.png" alt="Logo" width="200px" height="250px">
  </a>

<h2 align="center">TALLA-RAG</h2>

</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#because-of-why">Because of Why ?</a></li>
    <li><a href="#usage">Usage</a></li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
<h2 id="about-the-project">About The Project</h2>


<h2 id="built-with">Built with</h2>

[![Cassandra][Cassandra-badge]][Cassandra-url]
[![Streamlit][Streamlit-badge]][Streamlit-url]
[![Docker][Docker-badge]][Docker-url]
[![Ollama][Ollama-badge]][Ollama-url]
[![Python][Python-badge]][Python-url]
[![UV][UV-badge]][UV-url]




[Ollama-badge]: https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white
[Ollama-url]: https://ollama.com

[Streamlit-badge]: https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white
[Streamlit-url]: https://streamlit.io

[Docker-badge]: https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/

[Cassandra-badge]: https://img.shields.io/badge/Cassandra-1287B1?style=for-the-badge&logo=apache-cassandra&logoColor=white
[Cassandra-url]: https://cassandra.apache.org/


[Python-badge]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/

[UV-badge]: https://img.shields.io/badge/UV-3A0CA3?style=for-the-badge&logo=python&logoColor=white
[UV-url]: https://github.com/astral-sh/uv



<p align="right">(<a href="#readme-top">back to top</a>)</p>


<h2 id="because-of-why-">Because of Why ?</h2>
This project was built as a means to experiment myself with NoSql databases. Building a project that implemented Cassandra helped me understand what actually NoSql databases are meant by and particularly the distributed nature Cassandra is famous for. This project helped me get closer to my high end Engineering aspirations and get in touch with uv for dependency management.

<!-- USAGE EXAMPLES -->
<h2 id="usage">Usage</h2>

[**TALLA-RAG**](https://github.com/nnay29/cassandra-cluster-RAG) is a local application that lets you chat with your documents using a local LLM backed by a Cassandra cluster for vector storage.

1. Upload a `.txt` or `.pdf` file via the sidebar.
2. Click **Ingest to Cluster** — chunks are embedded and stored across Cassandra nodes.
3. Ask questions in the chat — the app retrieves relevant chunks and answers using the LLM only.
4. Use **Clear All Knowledge** to wipe the vector store.

<!-- GETTING STARTED -->
<h2 id="getting-started">Getting Started</h2>

<h3 id="prerequisites">Prerequisites</h3>

- [Docker](https://www.docker.com/desktop/) & Docker Compose
- [Ollama](https://ollama.com/download) running locally with the following models pulled:
  ```sh
  ollama pull nomic-embed-text:v1.5
  ollama pull granite3.2:2b
  ollama pull <your_model_name> # in case you prefer another ollama model
  ollama pull <your_embedding_model> # or another embedding model...
  ```
  I recommend to [check your hardware's capabilities to run opensource LLMs](https://medium.com/@smrati.katiyar/check-your-hardwares-capabilities-to-run-opensource-llms-44dc70694468)
- [Python 3.11](https://www.python.org) or higher
- [uv](https://docs.astral.sh/uv/) (Python package manager) 
    ```sh
       pip install uv
    ```   

<h3 id="installation">Installation</h3>

1. Clone the repo
   ```sh
   git clone https://github.com/nnay29/cassandra-cluster-RAG.git
   cd cassandra-cluster-RAG
   ```
2. Copy and configure the environment file
    ```sh
    cp .env.example .env
    ```
   🚨 Edit .env and set _DOCKER_HOST_IP_ to you machine's local IP address.

3. Start the Cassandra cluster
   ```sh
   docker-compose up -d
   ```

4. Create a virtual environment

    ```sh
    uv venv
    ```
4. Install Python dependencies
   ```sh
   uv sync
   ```
5. Run the Streamlit app
   ```sh
   streamlit run app.py
   ```

   The app will be available at http://localhost:8501



<p align="right">(<a href="#readme-top">back to top</a>)</p>


<h2 id="troubleshooting">Troubleshooting</h2>


If you experience issues during the setup process or while running the app, please check the following:


| Issue Category | Specific Issue | Troubleshooting Solution |
|----------------|----------------|--------------------------|
| **Ollama Connection Error** | `ConnectionError: Failed to connect to Ollama. Please check that Ollama is downloaded, running and accessible.` | - *Check whether ollama is installed and running* - Also check if the model is pulled successfully|
| **Cluster Offline Error in app UI** | `Cluster Offline` (Cassandra cluster status) | *Wait for the Cassandra containers to finish starting up. Check logs if issue persists* |
| **Cluster Offline Error in app UI** | `Could not connect to Cassandra at <IP_ADRESS>:9042` – timeout error | *Make sure the env variable **DOCKER_HOST_IP** is set to your machine's local IP adress.* |
| **Cluster Offline Error in app UI** | `Cluster Offline` + `Could not connect to Cassandra at None: contact_points should not contain None (it can resolve to localhost)` | *Make sure the env variable **DOCKER_HOST_IP** is set to your machine's local IP adress.* |
| **Docker Compose Issues** | Docker Compose not working / not installed (Windows) | *Verify that you have Docker Desktop installed.* |
| **Docker Compose Issues** | Docker Compose not running | *Verify that Docker Compose is running. use docker compose ls command* |
| **Cassandra Containers Issues** | Cassandra containers not running | *Grab some coffee and wait for them to start up, if nothing happens after a while, check the logs.* |
| **Cassandra Containers Issues** | Cassandra logs show errors | *Check your Docker Compose logs for any error messages. Praise the lord too. I know what I mean...* |
| **Streamlit App Issues** | Streamlit app not running | *Verify that you activated the virtual environment and are in the right directory. Then use ```streamlit run app.py``` command* |
| **Streamlit App Issues** | Streamlit logs show errors | *Check your Streamlit logs for any error messages.* |

Open an [issue](https://github.com/nnay29/cassandra-cluster-RAG/issues) on the GitHub repository if you continue to experience issues. We will try to help you resolve them.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ROADMAP -->
<h2 id="roadmap">Roadmap</h2>

<!-- - [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature -->

See the [open issues](https://github.com/nnay29/cassandra-cluster-RAG/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>




<!-- CONTACT -->
<h2 id="contact">Contact</h2>

<!-- Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email@email_client.com -->

Project Link: [https://github.com/nnay29/cassandra-cluster-RAG](https://github.com/nnay29/cassandra-cluster-RAG)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
<h2 id="acknowledgments">Acknowledgments</h2>

* []()
* [Working on uv projects](https://docs.astral.sh/uv/guides/projects/)
* [Taximan Talla officiel](https://web.facebook.com/profile.php?id=61555192163930)
* [Top G](https://gemini.google.com/app)
* [Into the Unknown](https://chat.deepseek.com/)
* [It’s a human thing. You wouldn’t understand.](https://grok.com/)


<p align="right">(<a href="#readme-top">back to top</a>)</p>

