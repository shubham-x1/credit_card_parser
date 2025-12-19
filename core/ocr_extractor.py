import pytesseract
from pdf2image import convert_from_path

def extract_text_with_ocr(pdf_path):
    images = convert_from_path(pdf_path, dpi=300)

    full_text = ""
    for img in images:
        text = pytesseract.image_to_string(
            img,
            config="--oem 3 --psm 6"
        )
        full_text += text + "\n"

    return full_text
