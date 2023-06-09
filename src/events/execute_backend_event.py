import typing
import fastapi
from database.postgres.sql_db import connect_pg
from database.pinecone.vector_db import vector_db
from database.postgres.migrations import _1_create_jobs_table

def execute_backend_server_event_handler(backend_app: fastapi.FastAPI) -> typing.Any:
    async def launch_backend_server_events() -> None:
        vector_db.connect('nobrainer')
        await connect_pg()
        await _1_create_jobs_table.migrate()
    return launch_backend_server_events
