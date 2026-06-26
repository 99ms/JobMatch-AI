import pdfplumber


def extract_text_from_pdf(upload_file):
    text = ""

    with pdfplumber.open(upload_file.file) as pdf:
        page_count = len(pdf.pages)

        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text, page_count