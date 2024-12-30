import pytesseract
from langdetect import detect, DetectorFactory
from PIL import Image
from text_processor import TextProcessor


class OCRProcessor:
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        self.text_processor = TextProcessor()
        
    def extract_text(self, image_path, lang="eng"):
        try:
            image = Image.open(image_path)
            
            # Alteração: Usei o parâmetro 'lang' diretamente, sem usar 'self.language_mapping'
            raw_text = pytesseract.image_to_string(image, lang=lang)

            # Detecção de idioma (opcional e para debug, não necessária)
            try:
                detected_language = detect(raw_text)  # Alteração: Mantive o 'detect', mas não uso mais para alterar o idioma no Tesseract
                print(f"Idioma detectado: {detected_language}")  # Para debug
            except Exception as e:
                print(f"Erro ao detectar idioma: {e}")

            # Processamento do texto extraído
            processed_text = self.text_processor.process(raw_text)
            return processed_text
        except Exception as e:
            print(f"Erro OCR: {e}")
            return None
