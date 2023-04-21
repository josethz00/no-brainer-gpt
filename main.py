import openai
import pinecone
import os
from dotenv import load_dotenv
from unstructured.partition.auto import partition
from unstructured.staging.base import elements_to_json

load_dotenv()

openai.api_key = os.getenv("OPEN_AI_API_KEY")
MODEL = "text-embedding-ada-002"

elements = partition(filename="./storage/example.md")
print(elements_to_json(elements))