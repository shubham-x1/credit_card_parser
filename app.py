import os
import json

from core.pdf_detector import is_text_pdf
from core.text_extractor import extract_text
from core.ocr_extractor import extract_text_with_ocr
from core.parser import UniversalParser
from core.pdf_validator import is_valid_pdf

PDF_NAME = "credit_card_statement.pdf"
PDF_PATH = os.path.join("input_pdfs", PDF_NAME)


def main():
    print("Processing PDF...")

    # -------------------------------
    # 1. File existence check
    # -------------------------------
    if not os.path.exists(PDF_PATH):
        print("ERROR: PDF file not found.")
        print("Please place a PDF inside input_pdfs/sample.pdf")
        return

    # -------------------------------
    # 2. PDF validity check (CRITICAL)
    # -------------------------------
    if not is_valid_pdf(PDF_PATH):
        print("Detected image-based or malformed PDF")
        print("Attempting image-level OCR")

        print(
            "NOTE: This PDF appears to be generated from a screenshot "
            "or is internally malformed."
        )
        print(
            "For reliable processing, please upload an original "
            "bank e-statement PDF."
        )

        # In a real system, we FAIL FAST here to avoid instability
        # You could alternatively implement direct image OCR if needed
        return

    # -------------------------------
    # 3. Decide parsing strategy
    # -------------------------------
    if is_text_pdf(PDF_PATH):
        print("Text-based PDF detected")
        text = extract_text(PDF_PATH)
    else:
        print("Scanned PDF detected, running OCR")
        text = extract_text_with_ocr(PDF_PATH)
        print("OCR TEXT SAMPLE:\n", text[:1000])


    # -------------------------------
    # 4. Parse extracted text
    # -------------------------------
   
    parser = parser = UniversalParser()

    parsed_data = parser.parse(text)


    # -------------------------------
    # 5. Save output
    # -------------------------------
    os.makedirs("output", exist_ok=True)
    output_path = os.path.join("output", "result.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(parsed_data, f, indent=4)

    print("Extraction complete.")
    print(f"Output written to {output_path}")


if __name__ == "__main__":
    main()
