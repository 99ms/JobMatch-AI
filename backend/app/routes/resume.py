from fastapi import APIRouter

router = APIRouter(prefix="/resume", tags=["Resume"])


@router.get("/health")
def health():
    return {
        "status": "Resume route working!"
    }