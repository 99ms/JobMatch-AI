from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.routes.resume import router as resume_router

app = FastAPI(
    title="JobMatch API",
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

app.include_router(resume_router)


@app.get("/")
def root():
    return {
        "status": "online",
        "message": "JobMatch Backend is running!"
    }