from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from app import pipeline  # this uses your minimal pipeline

app = FastAPI(title="Haystack RAG API")

class QueryRequest(BaseModel):
    question: str
    top_k: int = 2

class Answer(BaseModel):
    answer: str
    score: float

class QueryResponse(BaseModel):
    question: str
    answers: List[Answer]

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/query", response_model=QueryResponse)
async def query_qa(request: QueryRequest):
    result = pipeline.run(
        query=request.question,
        params={"Retriever": {"top_k": request.top_k}, "Reader": {"top_k": 1}}
    )
    answers = [
        Answer(answer=result["answers"][0]["answer"], score=result["answers"][0]["score"])
    ]
    return QueryResponse(question=request.question, answers=answers)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
