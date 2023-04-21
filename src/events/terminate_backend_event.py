import typing

import loguru
import fastapi

def terminate_backend_server_event_handler(backend_app: fastapi.FastAPI) -> typing.Any:
    @loguru.logger.catch
    async def stop_backend_server_events() -> None:
        # await dispose_db_connection(backend_app=backend_app)
        pass

    return stop_backend_server_events
