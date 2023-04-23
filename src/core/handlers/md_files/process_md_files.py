import json
import os
import uuid
import openai
import asyncio
from unstructured.partition.md import partition_md
from unstructured.staging.base import elements_to_json
from database.pinecone.vector_db import vector_db
from fastapi import UploadFile

async def process_md_files(md_files: list[UploadFile], message_queue: asyncio.Queue):
    current_file = 0
    for md_file in md_files:
        openai.api_key = os.getenv("OPEN_AI_API_KEY")
        MODEL = "text-embedding-ada-002"

        elements = partition_md(file=md_file.file)  # partition the markdown file
        partitioned_text = json.loads(elements_to_json(elements))  # convert partitions into JSON and load into Python dict

        filtered_partitioned_text = [element["text"] for element in partitioned_text if "text" in element]
        batch_size = 500  # set the batch size to 500 because pinecone cannot handle the 1500+ embeddings at once

        # Add the embeddings to the Pinecone index
        for i in range(0, len(filtered_partitioned_text), batch_size):
            # Create an embedding for a single document using the text-embedding-ada-002 model
            embeddings_api_response = await asyncio.to_thread(
                openai.Embedding.create,
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
        current_file += 1
        await message_queue.put({
            "message": f"Finished processing {md_file.filename}.",
            "status": f"Processed {current_file} of {len(md_files)} files."
        })

    await message_queue.put({
        "message": "Finished processing all files.",
        "status": f"Done. {len(md_files)/len(md_files)} files processed."
    })
