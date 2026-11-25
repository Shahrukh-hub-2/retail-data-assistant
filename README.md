# Retail Data Assistant

A RAG (Retrieval-Augmented Generation) API that answers customer questions about store policies, using a made-up retail shop called **Desert Mart**.

Personal learning project, in progress. All data is fictional; no real company data is used.

## What it does

Ask a question like *"How long do card refunds take?"* and the API:
1. Turns the question into a vector with an embedding model
2. Finds the closest policy chunks in ChromaDB
3. Sends those chunks to Llama 3.2, which writes the answer
4. Returns the answer **with its sources**

If the answer isn't in the documents, it replies *"I don't know based on the store policies"* instead of guessing.

## Tech stack

| Part | Tool |
|---|---|
| API | FastAPI + Pydantic |
| Embeddings | nomic-embed-text (via Ollama) |
| Vector database | ChromaDB |
| LLM | Llama 3.2 (via Ollama, runs locally) |
| Language | Python 3.12 |

## How it works

```
Policy docs → chunks (60 words, 10 overlap) → embeddings → ChromaDB
Question → embedding → top-k closest chunks → Llama 3.2 → answer + sources
```

## Run it locally

1. Install [Ollama](https://ollama.com), then:
   ```bash
   ollama pull nomic-embed-text
   ollama pull llama3.2
   ```
2. Set up the project:
   ```bash
   git clone https://github.com/Shahrukh-hub-2/retail-data-assistant.git
   cd retail-data-assistant
   python3.12 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   python make_docs.py
   ```
3. Start the API:
   ```bash
   python -m uvicorn app.main:app --reload
   ```
4. Open `http://localhost:8000/docs` and try `POST /ask`:
   ```json
   {"question": "How long do card refunds take?", "top_k": 3}
   ```

## Roadmap

- [x] FastAPI endpoints with Pydantic validation
- [x] RAG pipeline: chunking, embeddings, ChromaDB, Llama 3.2
- [ ] Evaluation: test question set, recall@k, hallucination checks
- [ ] Agent with a SQL tool on sales data and a human approval step
- [ ] Docker, cloud deployment, Streamlit chat UI, CI/CD