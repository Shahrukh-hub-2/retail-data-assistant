from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Retail Data Assistant")


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
    sources = [f"doc_{i}" for i in range(1, q.top_k + 1)]
    return Answer(answer=f"You asked: {q.question}", sources=sources)