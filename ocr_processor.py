import pytesseract
from PIL import Image
from text_processor import TextProcessor


class OCRProcessor:
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        self.text_processor = TextProcessor()
    def extract_text(self, image_path):
        try:
            image = Image.open(image_path)
            raw_text = pytesseract.image_to_string(image)
            processed_text = self.text_processor.process(raw_text)
            return processed_text
        except Exception as e:
            print(f"Erro OCR: {e}")
            return None
    
    