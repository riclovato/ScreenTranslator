from googletrans import Translator as GoogleTranslator


class Translator:
    def __init__(self):
        self.google_translator = GoogleTranslator()
        self.lang_map = {
            "eng": "en",
            "chi_sim": "zh-cn",
            "chi_tra": "zh-tw",
            "fra": "fr",
            "spa": "es",
            "pt": "pt"
        }
    
    
    
    def translated_text(self, text, target_language="pt"):
        try:
            target = self.lang_map.get(target_language, target_language)
            translated = self.google_translator.translate(text, dest=target)
            return translated.text
        except Exception as e :
            print(f"Erro na tradução: {e}")
            return "Erro na tradução"