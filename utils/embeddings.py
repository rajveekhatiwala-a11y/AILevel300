"""
Embedding Utilities
Helper functions for working with embeddings
"""
import numpy as np
from typing import List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors
    
    Args:
        vec1: First vector
        vec2: Second vector
        
    Returns:
        Cosine similarity score
    """
    vec1_np = np.array(vec1)
    vec2_np = np.array(vec2)
    
    dot_product = np.dot(vec1_np, vec2_np)
    magnitude1 = np.linalg.norm(vec1_np)
    magnitude2 = np.linalg.norm(vec2_np)
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    return dot_product / (magnitude1 * magnitude2)


def batch_embeddings(texts: List[str], embedding_function, batch_size: int = 10) -> List[List[float]]:
    """
    Generate embeddings in batches
    
    Args:
        texts: List of texts to embed
        embedding_function: Function to generate embeddings
        batch_size: Batch size for processing
        
    Returns:
        List of embedding vectors
    """
    embeddings = []
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        batch_embeddings = [embedding_function(text) for text in batch]
        embeddings.extend(batch_embeddings)
        logger.info(f"Generated embeddings for batch {i // batch_size + 1}")
    
    return embeddings


def normalize_vector(vector: List[float]) -> List[float]:
    """
    Normalize a vector to unit length
    
    Args:
        vector: Input vector
        
    Returns:
        Normalized vector
    """
    vec_np = np.array(vector)
    magnitude = np.linalg.norm(vec_np)
    
    if magnitude == 0:
        return vector
    
    return (vec_np / magnitude).tolist()


def find_top_k_similar(query_embedding: List[float], 
                       embeddings: List[List[float]], 
                       k: int = 5) -> List[int]:
    """
    Find top K most similar embeddings
    
    Args:
        query_embedding: Query vector
        embeddings: List of embedding vectors
        k: Number of results to return
        
    Returns:
        Indices of top K similar embeddings
    """
    similarities = [
        cosine_similarity(query_embedding, emb) 
        for emb in embeddings
    ]
    
    # Get indices of top K similarities
    top_k_indices = np.argsort(similarities)[-k:][::-1]
    
    return top_k_indices.tolist()
