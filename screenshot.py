import tkinter as tk 
import pyautogui
from PIL import Image, ImageTk

class ScreenCapture:
    def __init__(self, main_window):
        self.root = main_window
        self.current_rect = None
        self.start_x = None
        self.start_y = None


    def capture_full(self):
        #minimiza a janela
        self.root.iconify()
        self.root.after(1000)

        #captura a tela
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        self.root.deiconify()
        print("Screenshot capturada!")
        return "screenshot.png"
    
    
    def capture_selection(self):
        #minimiza a janela
        self.root.iconify()

        #cria uma janela transparente em tela cheia
        self.selection_window = tk.Toplevel(self.root)
        self.selection_window.attributes('-fullscreen', True, '-alpha', 0.3)
        self.selection_window.configure(bg='grey')

        #eventos do mouse
        self.selection_window.bind('<Button-1>', self.start_rect)
        self.selection_window.bind('<B1-Motion>', self.draw_rect)
        self.selection_window.bind('<ButtonRelease-1>', self.end_rect)

        #canvas para desenhar a seleção
        self.canvas = tk.Canvas(self.selection_window, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
    
    
    def start_rect(self, event):
        self.start_x = event.x
        self.start_y = event.y

        #retangulo inicial
        if self.current_rect:
            self.canvas.delete(self.current_rect)
        self.current_rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=2
        )
    

    def draw_rect(self, event):
        #atualiza o retangulo enquanto o mouse se move
        if self.current_rect:
            self.canvas.coords(
                self.current_rect, self.start_x, self.start_y, event.x, event.y
            )
    

    def end_rect(self, event):
        #captura area selecionada
        x1 = min(self.start_x, event.x)
        y1 = min(self.start_y, event.y)
        x2 = max(self.start_x, event.x)
        y2 = max(self.start_y, event.y)

        #fecha a janela de seleção
        self.selection_window.destroy()
        self.root.deiconify()

        self.root.after(100)

        #captura a area selecionada
        screenshot = pyautogui.screenshot(region=(x1,y1,x2-x1, y2-y1))
        screenshot.save("screenshot.png")
        print("Área selecionada capturada!")
        return "screenshot.png"