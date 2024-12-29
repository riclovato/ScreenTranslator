import tkinter as tk
from screenshot import ScreenCapture


class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tradutor de Tela")

        #inicia o módulo de captura
        self.screen_capture = ScreenCapture(self.root)

        #botões
        self.btn_full = tk.Button(self.root, text="Capturar Tela Inteira", command=self.capture_full)
        self.btn_full.pack(pady=5)

        self.btn_selection = tk.Button(self.root, text="Selecionar Área", command=self.capture_selection)
        self.btn_selection.pack(pady=5)

    def capture_full(self):
        image_path = self.screen_capture.capture_full()
        print(f'Screenshot salva em: {image_path}')

    def capture_selection(self):
        self.screen_capture.capture_selection()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.run()