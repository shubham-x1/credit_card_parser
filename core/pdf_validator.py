import subprocess


def is_valid_pdf(pdf_path):
    try:
        subprocess.run(
            ["pdfinfo", pdf_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        return True
    except Exception:
        return False
