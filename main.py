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
partitioned_text = json.loads(elements_to_json(elements)) # convert partitions into JSON and load into Python dict

filtered_partitioned_text = [element for element in partitioned_text if "text" in element]