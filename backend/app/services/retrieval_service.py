from app.services.embedding_service import generate_embedding
from app.services.faiss_service import search_similar

def retrieve_similar_code(embedding,k=3):
    
    results=search_similar(embedding,k)
    return results