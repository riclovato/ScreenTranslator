from googletrans import Translator as GoogleTranslator


class Translator:
    def __init__(self):
        self.google_translator = GoogleTranslator()
    
    
    def translated_text(self, text, src_language = "auto", target_language="pt"):
        try:
            translated = self.google_translator.translate(text, src=src_language,dest=target_language)
            return translated.text
        except Exception as e :
            print(f"Erro na tradução: {e}")
            return None