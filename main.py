import pyautogui
import tkinter as tk 
from PIL import Image, ImageTk


class ScreenshotApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tradutor de Tela")

        #botões
        self.btn_full = tk.Button(self.root, text="Capturar Tela Inteira", command=self.capture_full)
        self.btn_full.pack(pady=5)

        self.btn_selection = tk.Button(self.root, text="Selecionar Área", command=self.capture_selection)
        self.btn_selection.pack(pady=5)

    def capture_full(self):
        #minimiza a janela
        self.root.iconify()
        self.root.after(1000)

        #captura a tela
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
    
    def capture_selection(self):
        print("Implementando")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ScreenshotApp()
    app.run()