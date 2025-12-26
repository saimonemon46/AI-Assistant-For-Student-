from services.llm_service import get_llm
from services.pdf_service import extract_text_from_pdf
from services.ocr_service import extract_text_from_image

class StudyAgent:
    def __init__(self):
        self.llm = get_llm()

    def handle_pdf(self, file_path: str) -> str:
        text = extract_text_from_pdf(file_path)
        return text

    def handle_image(self, file_path: str) -> str:
        text = extract_text_from_image(file_path)
        return text
