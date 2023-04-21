import openai
import pinecone
import os
import json
import uuid
from dotenv import load_dotenv
from unstructured.partition.md import partition_md
from unstructured.staging.base import elements_to_json

load_dotenv()

openai.api_key = os.getenv("OPEN_AI_API_KEY")
MODEL = "text-embedding-ada-002"

# Connect Pinecone
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENV")
)

# Create a Pinecone index
if 'nobrainer' not in pinecone.list_indexes():
    pinecone.create_index('nobrainer', dimension=1536) # set 1536 as the dimension of the embeddings, the default of the text-embedding-ada-002 model
# Connect to the index
index = pinecone.Index('nobrainer')


elements = partition_md(filename="./storage/example.md")
partitioned_text = json.loads(elements_to_json(elements)) # convert partitions into JSON and load into Python dict

filtered_partitioned_text = [element["text"] for element in partitioned_text if "text" in element]

# Create an embedding for a single document using the text-embedding-ada-002 model
embeddings_api_response = openai.Embedding.create(
    input=filtered_partitioned_text,
    engine=MODEL
)

embeddings = [record["embedding"] for record in embeddings_api_response["data"]]

# Add the embeddings to the Pinecone index
index.upsert_many(
    ids=[str(uuid.uuid4()) for _ in range(len(embeddings))],
    vectors=embeddings
)

query = input("Enter a query: ")
query_embedding = openai.Embedding.create(
    input=query,
    engine=MODEL
)['data'][0]['embedding']

# Search in the vector database for the closest vector to the query
results = index.query(
    [query_embedding],
    top_k=5,
    include_metadata=True
)

for match in results['matches']:
    print(f"{match['score']:.2f}: {match['metadata']['text']}")