import typing

import loguru
import fastapi
from database.pinecone.vector_db import vector_db

def terminate_backend_server_event_handler(backend_app: fastapi.FastAPI) -> typing.Any:
    @loguru.logger.catch
    async def stop_backend_server_events() -> None:
        vector_db.index.close()
    return stop_backend_server_events
