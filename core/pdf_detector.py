import pdfplumber

def is_text_pdf(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text and len(text.strip()) > 50:
                    return True
        return False
    except Exception:
        # Non-standard or scanned PDF → use OCR
        return False
