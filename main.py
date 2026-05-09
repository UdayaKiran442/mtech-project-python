from fastapi import FastAPI
from pydantic import BaseModel

from services.sentence_transformer import convert_text_to_embeddings_service

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

class SentenceRequest(BaseModel):
    sentence: str

@app.post("/text/embeddings")
def convert_text_to_embeddings(request: SentenceRequest):
    try:
        embeddings = convert_text_to_embeddings_service(request.sentence)
        return {"embeddings": embeddings}
    except Exception as e:
        if isinstance(e, RuntimeError):
            return {"error": str(e)}
        return {"error": "An unexpected error occurred in python service."}
