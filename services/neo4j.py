import os
from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph
from neo4j import GraphDatabase


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

try:
    driver.verify_connectivity()
    print("Successfully connected to Neo4j database.")
except Exception as e:
    print(f"Failed to connect to Neo4j database: {e}")
    driver.close()
    raise e