CHAT_MODEL = "llama3.2"
from pathlib import Path
import chromadb
import ollama

DOCS_DIR = Path("data/docs")
EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL = "llama3.2"

client = chromadb.PersistentClient(path="chroma_db")


def chunk_text(text, chunk_size=60, overlap=10):
    words = text.split()
    step = chunk_size - overlap
    chunks = []
    for start in range(0, len(words), step):
        chunks.append(" ".join(words[start:start + chunk_size]))
        if start + chunk_size >= len(words):
            break
    return chunks


def embed(texts):
    return ollama.embed(model=EMBED_MODEL, input=texts)["embeddings"]


def build_index():
    try:
        client.delete_collection("policies")
    except Exception:
        pass
    col = client.create_collection("policies")
    ids, docs, metas = [], [], []
    for path in DOCS_DIR.glob("*.md"):
        for i, chunk in enumerate(chunk_text(path.read_text())):
            ids.append(f"{path.stem}_{i}")
            docs.append(chunk)
            metas.append({"source": path.name})
    col.add(ids=ids, documents=docs, embeddings=embed(docs), metadatas=metas)
    return len(docs)


def retrieve(question, k=3):
    col = client.get_collection("policies")
    res = col.query(query_embeddings=embed([question]), n_results=k)
    sources = [m["source"] for m in res["metadatas"][0]]
    return res["documents"][0], sources


def answer(question, k=3):
    chunks, sources = retrieve(question, k)
    context = "\n\n".join(chunks)
    prompt = (
        "Answer the question using ONLY the context below. "
        "If the answer is not in the context, say: "
        "'I don't know based on the store policies.'\n\n"
        f"Context:\n{context}\n\nQuestion: {question}"
    )
    reply = ollama.chat(model=CHAT_MODEL, messages=[{"role": "user", "content": prompt}])
    return reply["message"]["content"], sources


if __name__ == "__main__":
    print("Chunks indexed:", build_index())
    ans, src = answer("How many days do I have to return electronics?")
    print("Answer:", ans)
    print("Sources:", src)