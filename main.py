from fastapi import FastAPI
from pydantic import BaseModel

from services.sentence_transformer import convert_text_to_embeddings_service
from services.neo4j import upsert_to_neo4j_service

app = FastAPI()

class IUpsertToNeo4j(BaseModel):
    text: str

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
    
@app.post("/neo4j/upsert")
def upsert_text_to_neo4j(payload: IUpsertToNeo4j):
    try:
        result = upsert_to_neo4j_service(payload.text)
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}