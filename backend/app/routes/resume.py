from fastapi import APIRouter, UploadFile, File, Form

from app.services.pdf_service import extract_text_from_pdf

from app.models.analysis import AnalysisRequest

from app.services.analysis_service import analyze_resume

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)


@router.get("/health")
def health():
    return {
        "status": "Resume route working!"
    }


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    text, pages = extract_text_from_pdf(file)

    return {
        "filename": file.filename,
        "pages": pages,
        "text": text
    }

@router.post("/analyze")
def analyze(request: AnalysisRequest):
    return analyze_resume(
        request.resume_text,
        request.job_description
    )

@router.post("/process")
async def process_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    text, pages = extract_text_from_pdf(file)

    analysis = analyze_resume(
        resume_text=text,
        job_description=job_description
    )

    return {
        "filename": file.filename,
        "pages": pages,
        "analysis": analysis
    }