# Task 3 – Local Semantic Search Engine

This project demonstrates how to build a CLI-based semantic search tool by leveraging **OpenAI embeddings** and GPT-4o for enhanced query responses. The application processes natural language queries and provides a context-driven answer by utilizing a local vector database.

## Features

- Document embedding using OpenAI’s `text-embedding-3-small` model.
- Local storage of embeddings using FAISS for efficient similarity search.
- Cosine similarity to find the top N most relevant document matches.
- Query enhancement with GPT-4o for generating a natural response.

## Components

- **OpenAI Embeddings**: Convert text into vectors for semantic similarity.
- **FAISS Index**: Efficiently store and search through document vectors.
- **GPT-4o**: Generate responses based on retrieved context.

## Folder Structure

```
Task 3/
├── main.py                  # Entry point: loads API key, initializes and runs the search application
├── semantic_search.py       # Handles corpus loading, querying, and interaction with GPT-4o
├── vector_store.py          # VectorStore class for managing FAISS index and document embeddings
├── .env                     # Contains your OpenAI API key
├── logs/                    # Auto-generated folder for session logs
├── corpus.txt               # Sample document corpus for the search engine
├── .gitignore               # gitignore file
└── README.md                # This file
```

## How to Run

1. **Install dependencies**

```bash
pip install openai faiss-cpu numpy python-dotenv
```

2. **Configure API Key:**

Create a `.env` file with the following content:

```
OPENAI_API_KEY=sk-...
```

3. **Start the Semantic Search:**

```bash
python main.py
```

4. **Interact with the Search Engine:**

- Enter your query in natural language.
- Type `exit` or `quit` to end the session.

## How It Works

1. **Embedding the Corpus**: Convert text from `corpus.txt` into embeddings using OpenAI’s API.
2. **Storing in FAISS Index**: Store normalized vectors for efficient cosine similarity search.
3. **Query Processing**: Take user queries, embed them, and retrieve the top matching documents.
4. **Query Enhancement with GPT-4o**: Use the context from top matches to generate a natural language response.

## Bonus Features

- **Reusable VectorStore Class**: Handles adding and searching text.
- **Inline Source Mapping**: GPT-4o responses with referenced sources.
- **Looped Interaction Mode**: Continuous query and response logging.
- **Automatic File Chunks**: Optional feature to handle large text files.

## Logging

Each session is logged with a timestamp, recording inputs and GPT-4o outputs. Logs can be found in the `logs/` directory.

---

## Notes

- Ensure your OpenAI API key is valid and has the necessary access.
- This project uses GPT-4o, which requires specific access from OpenAI.

Be sure to refer to the provided example `corpus.txt` to test the tool effectively.
