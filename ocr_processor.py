import pytesseract
from langdetect import detect, DetectorFactory
from PIL import Image, ImageEnhance, ImageFilter
from text_processor import TextProcessor
from dataclasses import dataclass
from typing import List, Tuple
import os

@dataclass
class TextBlock:
    text: str
    position: Tuple[int, int, int, int]
    confidence: float

class OCRProcessor:
    def __init__(self):
        # Verifica e configura o caminho do Tesseract
        tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        if not os.path.exists(tesseract_path):
            raise Exception(f"Tesseract não encontrado em {tesseract_path}")
            
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        # Verifica se os arquivos de idioma existem
        tessdata_dir = os.path.join(os.path.dirname(tesseract_path), 'tessdata')
        os.environ['TESSDATA_PREFIX'] = tessdata_dir
        
        self.text_processor = TextProcessor()
        
        # Lista de idiomas suportados
        self.supported_languages = {
            'eng': 'eng.traineddata',
            'chi_sim': 'chi_sim.traineddata',
            'chi_tra': 'chi_tra.traineddata',
            'fra': 'fra.traineddata',
            'spa': 'spa.traineddata',
            'por': 'por.traineddata',  # Note que para português usamos 'por.traineddata'
        }
        
        # Verifica arquivos de idioma
        self._verify_language_files(tessdata_dir)

    def preprocess_image(self, image_path):
        """Pré-processa a imagem para melhorar o reconhecimento de texto"""
        try:
            # Abre a imagem
            image = Image.open(image_path)
            
            # Converte para escala de cinza
            image = image.convert('L')
            
            # Aumenta o contraste
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            
            # Aplica filtro de nitidez
            image = image.filter(ImageFilter.SHARPEN)
            
            return image
            
        except Exception as e:
            print(f"Erro no pré-processamento da imagem: {e}")
            return None
    
    def _verify_language_files(self, tessdata_dir):
        missing_languages = []
        for lang, filename in self.supported_languages.items():
            if not os.path.exists(os.path.join(tessdata_dir, filename)):
                missing_languages.append(f"{lang} ({filename})")
        
        if missing_languages:
            raise Exception(f"Arquivos de idioma faltando: {', '.join(missing_languages)}\n"
                          f"Por favor, baixe-os de https://github.com/tesseract-ocr/tessdata e "
                          f"coloque em {tessdata_dir}")

    def extract_text(self, image_path, lang="eng"):
        try:
            # Correção para o português
            if lang == "por":
                lang = "por"  # Mantemos como "por" para o Tesseract
            
            processed_image = self.preprocess_image(image_path)
            if not processed_image:
                return None
                
            # Extração do texto
            config = '--psm 6'
            raw_text = pytesseract.image_to_string(processed_image, lang=lang, config=config)
            
            if not raw_text.strip():
                print(f"Nenhum texto encontrado na imagem para o idioma {lang}")
                return None
                
            # Processamento do texto extraído
            processed_text = self.text_processor.process(raw_text)
            return processed_text
            
        except Exception as e:
            print(f"Erro no OCR: {str(e)}")
            return None

    def extract_text_with_positions(self, image_path, lang="eng") -> List[TextBlock]:
        """Extrai texto com informações de posicionamento"""
        try:
            # Correção para o português
            if lang == "por":
                lang = "por"  # Mantemos como "por" para o Tesseract
                
            processed_image = self.preprocess_image(image_path)
            if not processed_image:
                return []
            
            # Configuração para melhor detecção de blocos de texto
            config = r'--oem 3 --psm 11'
            data = pytesseract.image_to_data(processed_image, lang=lang, config=config, output_type=pytesseract.Output.DICT)

            text_blocks = []
            for i in range(len(data['text'])):
                # Filtra apenas textos com confiança maior que 60% e não vazios
                if float(data['conf'][i]) > 60 and data['text'][i].strip():
                    text = self.text_processor.process(data['text'][i])
                    if text:
                        block = TextBlock(
                            text=text,
                            position=(
                                data['left'][i],
                                data['top'][i],
                                data['width'][i],
                                data['height'][i]
                            ),
                            confidence=float(data['conf'][i])
                        )
                        text_blocks.append(block)
            
            return text_blocks
        
        except Exception as e:
            print(f"Erro no OCR: {e}")
            return []