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

batch_size = 500 # set the batch size to 500 because pinecone cannot handle the 1500+ embeddings at once
# Add the embeddings to the Pinecone index
for i in range(0, len(filtered_partitioned_text), batch_size):
    # Create an embedding for a single document using the text-embedding-ada-002 model
    embeddings_api_response = openai.Embedding.create(
        input=filtered_partitioned_text,
        engine=MODEL
    )

    embeddings = [record["embedding"] for record in embeddings_api_response["data"]]

    to_upsert = [
        {
            "id": str(uuid.uuid4()),
            "values": embedding,
            "metadata": {
                "text": filtered_partitioned_text[j]
            }
        } for j, embedding in enumerate(embeddings)
    ]

    index.upsert(
        vectors=to_upsert,
    )

query = input("Enter a query: ")
query_embedding = openai.Embedding.create(
    input=query,
    engine=MODEL
)['data'][0]['embedding']

# Search in the vector database for the closest vector to the query
results = index.query(
    [query_embedding],
    top_k=10,
    include_metadata=True
)

prompt_gpt = [{'role': 'user', 'content': f"THE QUESTION IS: '{query}' \n\n"}]
context_gpt = "THE CONTEXT IS: "
for match in results['matches']:
    context_gpt += f"{match['score']:.3f}: {match['metadata']['text']}\n"
    print(f"{match['score']:.3f}: {match['metadata']['text']}")

context_gpt += "\n\n IF NECESSARY, complement the answer with your own information, or ask for more information."
prompt_gpt[0]['content'] += context_gpt

print(prompt_gpt)

# Call ChatGPT to generate a response
response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=prompt_gpt,
    temperature=0.6,
    max_tokens=2000,
    top_p=1.0,
    presence_penalty=0.0,
)

# Print the response
print('\n\n', response['choices'][0]['message']['content'])

# delete the index data
index.delete(delete_all=True)