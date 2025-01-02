import pytesseract
from langdetect import detect, DetectorFactory
from PIL import Image, ImageEnhance, ImageFilter
from text_processor import TextProcessor


class OCRProcessor:
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        self.text_processor = TextProcessor()
    
    def preprocess_image(self, image_path):
        try:
            image = Image.open(image_path)
            # converte a imagem para escala de cinza
            image = image.convert('L')
            # melhora o contraste
            image = ImageEnhance.Contrast(image).enhance(2)
            # filtro de nitidez
            image = image.filter(ImageFilter.SHARPEN)
            return image
        except Exception as e:
            print(f"Erro no pré-processamento da imagem : {e}")
            return None

        
    def extract_text(self, image_path, lang="eng"):
        try:
           processed_image = self.preprocess_image(image_path)
           if not processed_image:
                return None
           # extração do texto
           config = '--psm 6'  # PSM 6: Assume um bloco uniforme de texto
           raw_text = pytesseract.image_to_string(processed_image, lang=lang)

           #processamento do texto extraído
           processed_text = self.text_processor.process(raw_text)
           return processed_text
        except Exception as e:
            print(f"Erro no OCR: {e}")
            return None

