import openai
import pinecone
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPEN_AI_API_KEY")
MODEL = "text-embedding-ada-002"