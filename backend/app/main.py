from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints.resume import router as resume_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-powered resume and job matching platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Note: As per architecture freeze, not versioning the API yet (/api/v1)
app.include_router(resume_router)

@app.get("/")
def root():
    return {
        "status": "online",
        "message": f"{settings.PROJECT_NAME} Backend is running!"
    }