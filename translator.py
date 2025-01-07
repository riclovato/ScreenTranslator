from googletrans import Translator as GoogleTranslator
import time

class Translator:
    def __init__(self):
        self.google_translator = GoogleTranslator()
        self.lang_map = {
            "eng": "en",
            "chi_sim": "zh-cn",
            "chi_tra": "zh-tw",
            "fra": "fr",
            "spa": "es",
            "por": "pt"
        }
    
    def translated_text(self, text, target_language="por"):
        try:
            if not text or not isinstance(text, str):
                print(f"Texto inválido para tradução: {text}")
                return None
                
            target = self.lang_map.get(target_language, target_language)
            if not target:
                print(f"Idioma de destino inválido: {target_language}")
                return None
            
            # Adiciona um pequeno delay para evitar sobrecarga da API
            #time.sleep(0.01)
            
            # Garante que o texto está em formato string e limpo
            text = str(text).strip()
            if not text:
                return None
            
            # Tenta reconectar o tradutor se necessário
            try:
                translated = self.google_translator.translate(text, dest=target)
            except:
                print("Reconectando ao serviço de tradução...")
                self.google_translator = GoogleTranslator()
                time.sleep(1)
                translated = self.google_translator.translate(text, dest=target)
            
            if translated and hasattr(translated, 'text'):
                return translated.text
            return None
            
        except Exception as e:
            print(f"Erro na tradução: {str(e)}")
            # Tenta recriar o tradutor em caso de erro
            try:
                self.google_translator = GoogleTranslator()
            except:
                pass
            return None