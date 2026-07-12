from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from starlette.concurrency import run_in_threadpool
from app.schemas.resume import AnalysisResponse, SkillCategory, Statistics
from app.services.pdf_service import extract_text_from_pdf_bytes
from app.services.analysis_service import analyze_resume

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)

@router.get("/health")
def health():
    return {"status": "Resume route working!"}

@router.post("/analyze", response_model=AnalysisResponse)
async def process_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    file_bytes = await file.read()
    
    text, pages = await run_in_threadpool(extract_text_from_pdf_bytes, file_bytes)
    
    if not text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from PDF")

    analysis = analyze_resume(
        resume_text=text,
        job_description=job_description
    )

    # Convert the dict structure into the Pydantic Response Model
    return AnalysisResponse(
        filename=file.filename,
        match_score=analysis["match_score"],
        matching_keywords=analysis["matching_keywords"],
        missing_keywords=analysis["missing_keywords"],
        matched_skills=[SkillCategory(**cat) for cat in analysis["matched_skills"]],
        missing_skills=[SkillCategory(**cat) for cat in analysis["missing_skills"]],
        statistics=Statistics(**analysis["statistics"])
    )
