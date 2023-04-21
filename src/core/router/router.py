import fastapi

from core.router import qa_router

router = fastapi.APIRouter()
@router.get(
    path="/",
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_root():
    return {"message": "Hello World"}
router.include_router(router=qa_router.qa_router)
