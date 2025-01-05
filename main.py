import tkinter as tk
from screenshot import ScreenCapture
from ocr_processor import OCRProcessor
from translator import Translator

class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tradutor de Tela")
        self.language_mapping = {
            "Inglês": "eng",
            "Chinês Simplificado": "chi_sim",
            "Chinês Tradicional": "chi_tra",
            "Francês": "fra",
            "Espanhol": "spa",
            "Portugês": "pt",
        }
        self.source_language = tk.StringVar(value="Inglês")
        self.target_language = tk.StringVar(value="Portugês")
        #inicia o módulo de captura
        self.screen_capture = ScreenCapture(self.root)
        
        #menu de idiomas
        tk.Label(self.root, text="Selecione o Idioma de Origem:").pack(pady=5)
        self.language_menu = tk.OptionMenu(
            self.root, self.source_language, *self.language_mapping.keys()
        )
        self.language_menu.pack(pady=5)

        #botões
        self.btn_full = tk.Button(self.root, text="Capturar Tela Inteira", command=self.capture_full)
        self.btn_full.pack(pady=5)

        self.btn_selection = tk.Button(self.root, text="Selecionar Área", command=self.capture_selection)
        self.btn_selection.pack(pady=5)

        self.text_output = tk.Text(self.root, height=10, width=50)
        self.text_output.pack(pady=5)
        
        self.text_tranlated = tk.Text(self.root, height=20, width=50)
        self.text_tranlated.pack(pady=5)

        tk.Label(self.root, text = "Idioma de Destino: ").pack(pady=5)
        self.translation_menu = tk.OptionMenu(
            self.root, self.target_language, *self.language_mapping.keys()
        )
        self.translation_menu.pack(pady=5)

        self.ocr = OCRProcessor()
        self.translator = Translator()

    def capture_full(self):
        image_path = self.screen_capture.capture_full()
        selected_lang = self.language_mapping[self.selected_language.get()]
        text = self.ocr.extract_text(image_path, selected_lang)
        print(f'Texto extraído: {text}')

    def capture_selection(self):
        image_path = self.screen_capture.capture_selection()
        if image_path:
            selected_lang = self.language_mapping[self.source_language.get()]
            text = self.ocr.extract_text(image_path, selected_lang)
            self.display_text(text)
            self.display_translated_text(text)
    
    def display_text(self, text):
        self.text_output.delete('1.0', tk.END)
        if text:
            self.text_output.insert('1.0', text)
        else:
            self.text_output.insert('1.0', "Nenhum texto encontrado")
    
    def display_translated_text(self, text):
        self.text_tranlated.delete('1.0', tk.END)
        if text:
            selected_target = self.target_language.get()
            target_lang = self.language_mapping[selected_target]
            translated_text = self.translator.translated_text(text,target_lang)
            print(target_lang)
            if translated_text:
                self.text_tranlated.insert('1.0', translated_text)
            else:
                self.text_translated.insert('1.0', "Erro na Tradução")
        else:
            self.text_tranlated.insert('1.0', "Nenhum texto encontrado")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.run()