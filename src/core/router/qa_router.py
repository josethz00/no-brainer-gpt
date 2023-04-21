import fastapi

qa_router = fastapi.APIRouter(prefix="/qa", tags=["qa"])

@qa_router.post(
    path="/answer",
    status_code=fastapi.status.HTTP_201_OK,
)
async def generate_answers():
    return {"message": "Hello World"}
