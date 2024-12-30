import re
from typing import Optional
import string

class TextProcessor:
    def __init__(self):
        self.common_ocr_errors = {
            '|': 'I',
            '0': 'O',
            '1': 'l',
            '{': '(',
            '}': ')',
            '[': '(',
            ']': ')'
        }
    
    def process(self, text: str) -> Optional[str]:
        if not text:
            return None
            
        text = self._remove_noise(text)
        text = self._fix_common_errors(text)
        text = self._format_text(text)
        return text
    
    def _remove_noise(self, text: str) -> str:
        # Remove caracteres especiais e espaços extras
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text
    
    def _fix_common_errors(self, text: str) -> str:
        # Corrige erros comuns de OCR
        for error, fix in self.common_ocr_errors.items():
            text = text.replace(error, fix)
        return text
    
    def _format_text(self, text: str) -> str:
        # Normaliza quebras de linha e pontuação
        text = re.sub(r'([.!?])\s*(\n|\r\n)*\s*', r'\1\n', text)
        return text.strip()