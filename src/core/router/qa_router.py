import asyncio
import json
import os
import uuid
import fastapi
import openai
from sse_starlette import EventSourceResponse
from unstructured.partition.md import partition_md
from unstructured.staging.base import elements_to_json
from core.handlers.md_files.process_md_files import process_md_files
from database.pinecone.vector_db import vector_db
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi import Request, UploadFile, File, BackgroundTasks
import uuid

asyncio_mq = asyncio.Queue()

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

    print(results)

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

    return JSONResponse(
        content={
            "answer": response['choices'][0]['message']['content']
        }
    )

@qa_router.post(path='/upload-files/form', status_code=fastapi.status.HTTP_202_ACCEPTED)
async def upload_files_form(md_files: list[UploadFile] = File(...), background_tasks: BackgroundTasks = None):
    if len(md_files) > 10:
        raise fastapi.HTTPException(status_code=400, detail="Too many files! Max 10 files.")
    if not md_files:
        raise fastapi.HTTPException(status_code=400, detail="No files provided!")

    background_tasks.add_task(process_md_files, md_files=md_files, asyncio_queue=asyncio_mq)

    return {"status": "Processing"}

@qa_router.get(path='/upload-files/stream', status_code=fastapi.status.HTTP_200_OK)
async def event_stream(request: Request):
    async def event_generator():
        while True:
            print('aaaa')
            if await request.is_disconnected():
                print("something disconnected.")
                break

            if not asyncio_mq.empty():
                message = await asyncio_mq.get()
                print(f"Retrieved message from queue: {message}")
                yield {
                    "event": "message",
                    "id": uuid.uuid4(),
                    "retry": 4000,
                    "data": message,
                }

                if message == "Finished processing all files.":
                    break

                await asyncio.sleep(4)

    return EventSourceResponse(event_generator())

@qa_router.get(path='/search', status_code=fastapi.status.HTTP_200_OK)
async def search(search_term: str):
    # generate embeddings for the search term
    openai.api_key = os.getenv("OPEN_AI_API_KEY")
    MODEL = "text-embedding-ada-002"

    search_term_embeddings = openai.Embedding.create(
        input=search_term,
        engine=MODEL
    )['data'][0]['embedding']

    # Search in the vector database for the closest vector to the query
    results = vector_db.index.query(
        [search_term_embeddings],
        top_k=15,
        include_metadata=True
    )

    json_results = []

    for match in results['matches']:
        json_results.append({
            "score": match['score'],
            "text": match['metadata']['text']
        })

    return {
        "results": json_results
    }
