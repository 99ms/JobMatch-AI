from fastapi import APIRouter, UploadFile, File

from app.services.pdf_service import extract_text_from_pdf

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