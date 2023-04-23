import json
import os
import uuid
import fastapi
import openai
from unstructured.partition.md import partition_md
from unstructured.staging.base import elements_to_json
from core.handlers.md_files.process_md_files import process_md_files
from database.pinecone.vector_db import vector_db
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi import UploadFile, File, BackgroundTasks

class AnswerRequest(BaseModel):
    question: str

qa_router = fastapi.APIRouter(prefix="/qa", tags=["qa"])

@qa_router.post(
    path="/answer",
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def generate_answers(answer_request: AnswerRequest):
    openai.api_key = os.getenv("OPEN_AI_API_KEY")
    MODEL = "text-embedding-ada-002"

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

    vector_db.index.upsert(
        vectors=to_upsert,
    )

    prompt_query = answer_request.question
    query_embedding = openai.Embedding.create(
        input=prompt_query,
        engine=MODEL
    )['data'][0]['embedding']

    # Search in the vector database for the closest vector to the query
    results = vector_db.index.query(
        [query_embedding],
        top_k=10,
        include_metadata=True
    )

    prompt_gpt = [{'role': 'user', 'content': f"THE QUESTION IS: '{prompt_query}' \n\n"}]
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
    vector_db.index.delete(delete_all=True)

    return JSONResponse(
        content={
            "answer": response['choices'][0]['message']['content']
        }
    )

@qa_router.post(path='/upload-files', status_code=fastapi.status.HTTP_202_ACCEPTED)
async def upload_files(md_files: list[UploadFile] = File(...), background_tasks: BackgroundTasks =  None):
    if len(md_files) > 10:
        raise fastapi.HTTPException(status_code=400, detail="Too many files! Max 10 files.")
    if not md_files:
        raise fastapi.HTTPException(status_code=400, detail="No files provided!")
    background_tasks.add_task(process_md_files, md_files) # add the task to the background tasks
    return {"filenames": [file.filename for file in md_files], "status": "PROCESSING"}

