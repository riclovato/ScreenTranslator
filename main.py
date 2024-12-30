import tkinter as tk
from screenshot import ScreenCapture
from ocr_processor import OCRProcessor


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
        }
        self.selected_language = tk.StringVar(value="Inglês")
        #inicia o módulo de captura
        self.screen_capture = ScreenCapture(self.root)
        
        #menu de idiomas
        tk.Label(self.root, text="Selecione o Idioma:").pack(pady=5)
        self.language_menu = tk.OptionMenu(
            self.root, self.selected_language, *self.language_mapping.keys()
        )
        self.language_menu.pack(pady=5)

        #botões
        self.btn_full = tk.Button(self.root, text="Capturar Tela Inteira", command=self.capture_full)
        self.btn_full.pack(pady=5)

        self.btn_selection = tk.Button(self.root, text="Selecionar Área", command=self.capture_selection)
        self.btn_selection.pack(pady=5)

        self.text_output = tk.Text(self.root, height=10, width=50)
        self.text_output.pack(pady=5)

        self.ocr = OCRProcessor()

    def capture_full(self):
        image_path = self.screen_capture.capture_full()
        selected_lang = self.language_mapping[self.selected_language.get()]
        text = self.ocr.extract_text(image_path, selected_lang)
        print(f'Texto extraído: {text}')

    def capture_selection(self):
        image_path = self.screen_capture.capture_selection()
        if image_path:
            selected_lang = self.language_mapping[self.selected_language.get()]
            text = self.ocr.extract_text(image_path, selected_lang)
            self.display_text(text)
    
    def display_text(self, text):
        self.text_output.delete('1.0', tk.END)
        if text:
            self.text_output.insert('1.0', text)
        else:
            self.text_output.insert('1.0', "Nenhum texto encontrado")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.run()