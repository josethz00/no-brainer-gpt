import typing
import fastapi
from database.pinecone.vector_db import vector_db

def execute_backend_server_event_handler(backend_app: fastapi.FastAPI) -> typing.Any:
    async def launch_backend_server_events() -> None:
        vector_db.connect('nobrainer')
    return launch_backend_server_events
