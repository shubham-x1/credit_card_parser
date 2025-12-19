from PIL import Image
import pytesseract

# If needed on Windows
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

img = Image.open("st.jpg")
text = pytesseract.image_to_string(img)
img.save("scanned_statement.pdf", "PDF", resolution=300.0)

print("OCR OUTPUT:")
print(text)
