import os
import fastapi
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from events import terminate_backend_event, execute_backend_event
from core.router import router
from dotenv import load_dotenv

load_dotenv()

def initialize_backend_application() -> fastapi.FastAPI:
    app = fastapi.FastAPI()  # type: ignore

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_event_handler(
        "startup",
        execute_backend_event.execute_backend_server_event_handler(backend_app=app),
    )
    app.add_event_handler(
        "shutdown",
        terminate_backend_event.terminate_backend_server_event_handler(backend_app=app),
    )
    app.include_router(router=router.router)

    return app


backend_app: fastapi.FastAPI = initialize_backend_application()

if __name__ == "__main__":
    os.environ["PYTHONUNBUFFERED"] = "1"
    uvicorn.run(
        app="main:backend_app",
        host='0.0.0.0',
        port=5001,
        reload=True,
        workers=4,
        log_level='info',
    )
