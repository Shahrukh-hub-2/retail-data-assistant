from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from rag.pipeline import answer, build_index

app = FastAPI(title="Retail Data Assistant")

build_index()


class Question(BaseModel):
    question: str = Field(min_length=1)
    top_k: int = Field(default=3, ge=1, le=10)


class Answer(BaseModel):
    answer: str
    sources: list[str]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=Answer)
def ask(q: Question):
    try:
        text, sources = answer(q.question, k=q.top_k)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"RAG failed: {e}")
    return Answer(answer=text, sources=sources)