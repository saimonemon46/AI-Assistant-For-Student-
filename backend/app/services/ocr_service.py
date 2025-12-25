from PIL import Image
import pytesseract

def extract_text_from_image(path: str) -> str:
    text = pytesseract.image_to_string(Image.open(path))
    return text.strip() if text.strip() else "[No text detected in the image]"
