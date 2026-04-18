import os
from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph
from neo4j import GraphDatabase
from langchain_core.documents import Document
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_openai import ChatOpenAI 

load_dotenv()

url = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")
database = os.getenv("NEO4J_DATABASE")

graph_instance = Neo4jGraph(
    url=url,
    username=username,
    password=password,
    database=database
)

driver = GraphDatabase.driver(uri=url, auth=(username, password))

llm = ChatOpenAI(  
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0  
)

try:
    driver.verify_connectivity()
    print("Successfully connected to Neo4j database.")
except Exception as e:
    print(f"Failed to connect to Neo4j database: {e}")
    driver.close()
    raise e


def upsert_to_neo4j_service(text: str):
    try:
        llm_transformer = LLMGraphTransformer(llm=llm)
        documents = [Document(page_content=text)]
        graph_documents = llm_transformer.convert_to_graph_documents(documents)

        #  Extract nodes and relationships into plain dicts
        nodes = [
            {
                "id": node.id,
                "labels": node.type,  # e.g. "Person", "Organization"
                "properties": node.properties
            }
            for doc in graph_documents for node in doc.nodes
        ]
        

        relationships = [
            {
                "source": rel.source.id,
                "target": rel.target.id,
                "type": rel.type,
                "properties": rel.properties
            }
            for doc in graph_documents for rel in doc.relationships
        ]

        if not nodes:
            return "No graph data extracted from text."

        # Fallback query if APOC is not available
        node_query = """
            UNWIND $nodes AS node
            MERGE (n:Entity {id: node.id})
            SET n += node.properties
            SET n.label = node.labels
        """

        rel_query = """
            UNWIND $relationships AS rel
            MATCH (source {id: rel.source})
            MATCH (target {id: rel.target})
            MERGE (source)-[r:RELATES {type: rel.type}]->(target)
            SET r += rel.properties
        """

        graph_instance.query(node_query, params={"nodes": nodes})
        graph_instance.query(rel_query, params={"relationships": relationships})

        return f"Upserted {len(nodes)} nodes and {len(relationships)} relationships successfully."

    except Exception as e:
        return f"An error occurred while upserting to Neo4j: {str(e)}"