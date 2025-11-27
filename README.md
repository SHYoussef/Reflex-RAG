# Documentation

## RAG Template for Retrieval-Augmented Generation Applications

This README documents a template designed for building Retrieval-Augmented Generation (RAG) based applications. RAG systems combine information retrieval with generative AI models to provide more accurate and contextually relevant responses by incorporating external data sources.

### Purpose
Provides a foundational template structure for developers implementing RAG architecture in their applications.


### Usage
This template serves as a starting point for projects that require:
- Document retrieval and indexing
- Query processing and context enrichment
- Generation of responses based on retrieved information
- Semantic search capabilities

### Installation

Install the UV package manager and sync dependencies:
```bash
uv sync
```

### Configuration & Data

This project uses TOML files for configuration and a small set of environment variables.

- `config/agent.toml`: configuration settings for the RAG/agent components.
- `config/indexer.toml`: configuration settings for the indexing pipeline (paths, chunk sizes, index names, Pinecone settings, etc.).

.env file:
- Copy the provided template and set your secrets and keys before running the app or indexer.

PowerShell:
```
Copy-Item .env.template .env
```
Unix/macOS (bash):
```
cp .env.template .env
```

Open the newly created `./.env` and set the required variables (examples present in `.env.template`, such as `openai_api_key` and `pinecone_api_key`).

Data folder:
- Put your source documents in the `data/` folder. Current supported input type: PDF files only. Place PDFs directly under `data/` (or subfolders) so the indexer can discover and process them.

### Indexing

The repository includes a simple indexing script that reads configuration from `config/indexer.toml` and environment variables, loads PDF documents from the `data/` folder, splits them into chunks, and pushes embeddings to the configured index provider.

- Ensure `config/indexer.toml` is configured with the correct `folder_path` (where your PDFs live) and index settings.
- Ensure `.env` contains your API keys (e.g., Pinecone and OpenAI keys) before running the indexer.

Run the indexer from the project root:
```
python indexing.py
```

The script will create or update the index as configured and upload document embeddings.


### Running the Application

Start the application using uvicorn:
```bash
uvicorn main:fastapi_app
```

### Interface

The application uses [Chainlit](https://chainlit.io/) for the conversational interface. The Chainlit application is available at the `/interface` route.

### RAG Agent Example

![RAG Agent Architecture](images/reflex_graph.png)
