import openai
import pinecone
import os
import json
from dotenv import load_dotenv
from unstructured.partition.md import partition_md
from unstructured.staging.base import elements_to_json

load_dotenv()

openai.api_key = os.getenv("OPEN_AI_API_KEY")
MODEL = "text-embedding-ada-002"

elements = partition_md(filename="./storage/example.md")
partitioned_text = json.loads(elements_to_json(elements))

filtered_partitioned_text = [text for text in partitioned_text if text["type"] == "text"]
print(partitioned_text[0]["text"])