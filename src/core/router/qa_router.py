import fastapi

qa_router = fastapi.APIRouter(prefix="/qa", tags=["qa"])

@qa_router.get(
    path="/questions",
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_questions():
    return {"message": "Hello World"}
