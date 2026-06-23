from fastapi import APIRouter

router = APIRouter(
    prefix="/notifications",
    tags=["notifications"]
)

@router.get("/")
def get_notifications():
    return {"message": "Notification router is working!"}