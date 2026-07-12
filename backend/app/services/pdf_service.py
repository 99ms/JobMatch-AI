import pdfplumber
import io

def extract_text_from_pdf_bytes(file_bytes: bytes) -> tuple[str, int]:
    text = ""
    # Parse PDF directly from bytes in memory
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        page_count = len(pdf.pages)
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
                
    return text, page_count