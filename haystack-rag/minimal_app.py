from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import json

app = FastAPI(title="Minimal RAG API")

# Simple in-memory document store - no external dependencies
documents = [
    {"id": 1, "content": "Haystack is an open-source framework for building RAG pipelines."},
    {"id": 2, "content": "FastAPI is a modern Python web framework for APIs."},
    {"id": 3, "content": "Kubernetes orchestrates containerized applications."},
    {"id": 4, "content": "Docker is a containerization platform for packaging applications."},
    {"id": 5, "content": "Python is a popular programming language for AI and web development."}
]

class QueryRequest(BaseModel):
    question: str
    top_k: int = 2

class Answer(BaseModel):
    answer: str
    score: float

class QueryResponse(BaseModel):
    question: str
    answers: List[Answer]

def simple_search(query, top_k=3):
    """Simple keyword-based search without any ML libraries"""
    query_words = query.lower().split()
    scored_docs = []
    
    for doc in documents:
        content_lower = doc["content"].lower()
        score = sum(1 for word in query_words if word in content_lower)
        if score > 0:
            scored_docs.append({
                "content": doc["content"],
                "score": score / len(query_words),
                "id": doc["id"]
            })
    
    scored_docs.sort(key=lambda x: x["score"], reverse=True)
    return scored_docs[:top_k]

def simple_answer_extraction(query, documents):
    """Simple answer extraction without ML models"""
    if documents:
        best_doc = documents[0]
        query_words = query.lower().split()
        sentences = best_doc["content"].split(". ")
        
        for sentence in sentences:
            if any(word in sentence.lower() for word in query_words):
                return sentence.strip()
        
        return sentences[0].strip()
    
    return "I couldn't find a relevant answer."

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Minimal RAG API is running"}

@app.get("/")
async def root():
    return {"message": "Welcome to Minimal RAG API", "docs": "/docs"}

@app.post("/query", response_model=QueryResponse)
async def query_qa(request: QueryRequest):
    # Retrieve documents
    retrieved_docs = simple_search(request.question, request.top_k)
    
    # Extract answer
    answer = simple_answer_extraction(request.question, retrieved_docs)
    
    answers = [
        Answer(answer=answer, score=retrieved_docs[0]["score"] if retrieved_docs else 0.0)
    ]
    
    return QueryResponse(question=request.question, answers=answers)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 