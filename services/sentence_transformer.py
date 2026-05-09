from sentence_transformers import SentenceTransformer


def convert_text_to_embeddings_service(sentence: str) -> list:
    try:
        model = SentenceTransformer("all-MiniLM-L6-v2")
        return model.encode([sentence]).tolist()
    except Exception as e:
        raise RuntimeError(f"Failed to convert text to embeddings: {e}")
