from fastapi import FastAPI

from services.sentence_transformer import convert_text_to_embeddings_service

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/text/embeddings")
def convert_text_to_embeddings(sentences: list[str]):
    try:
        embeddings = convert_text_to_embeddings_service(sentences)
        return {"embeddings": embeddings}
    except Exception as e:
        if isinstance(e, RuntimeError):
            return {"error": str(e)}
        return {"error": "An unexpected error occurred in python service."}