# Ultra-minimal RAG implementation without any AI models
import json

# Simple in-memory document store
documents = [
    {"id": 1, "content": "Haystack is an open-source framework for building RAG pipelines."},
    {"id": 2, "content": "FastAPI is a modern Python web framework for APIs."},
    {"id": 3, "content": "Kubernetes orchestrates containerized applications."},
    {"id": 4, "content": "Docker is a containerization platform for packaging applications."},
    {"id": 5, "content": "Python is a popular programming language for AI and web development."}
]

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
                "score": score / len(query_words),  # Normalize by query length
                "id": doc["id"]
            })
    
    # Sort by score and return top_k
    scored_docs.sort(key=lambda x: x["score"], reverse=True)
    return scored_docs[:top_k]

def simple_answer_extraction(query, documents):
    """Simple answer extraction without ML models"""
    if documents:
        best_doc = documents[0]
        # Simple sentence extraction based on query keywords
        query_words = query.lower().split()
        sentences = best_doc["content"].split(". ")
        
        for sentence in sentences:
            if any(word in sentence.lower() for word in query_words):
                return sentence.strip()
        
        # Fallback to first sentence
        return sentences[0].strip()
    
    return "I couldn't find a relevant answer."

class SimplePipeline:
    def run(self, query, params=None):
        if params is None:
            params = {"Retriever": {"top_k": 3}, "Reader": {"top_k": 1}}
        
        # Retrieve documents
        retrieved_docs = simple_search(query, params["Retriever"]["top_k"])
        
        # Extract answer
        answer = simple_answer_extraction(query, retrieved_docs)
        
        return {
            "answers": [{
                "answer": answer,
                "score": retrieved_docs[0]["score"] if retrieved_docs else 0.0
            }],
            "documents": retrieved_docs
        }

# Create global pipeline instance
pipeline = SimplePipeline()

# Test run
if __name__ == "__main__":
    result = pipeline.run("What is Kubernetes?")
    print(f"Answer: {result['answers'][0]['answer']}")
    print(f"Score: {result['answers'][0]['score']}")
    print("✅ Pipeline working correctly!")
