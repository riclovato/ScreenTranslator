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
        self.root.iconify()
        self.root.after(1000)
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        self.root.deiconify()
        return "screenshot.png"
    
    def capture_selection(self):
        self.root.iconify()
        self.selection_window = tk.Toplevel(self.root)
        self.selection_window.attributes('-fullscreen', True, '-alpha', 0.3)
        self.selection_window.configure(bg='grey')
        
        self.canvas = tk.Canvas(self.selection_window, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        
        self.selection_window.bind('<Button-1>', self.start_rect)
        self.selection_window.bind('<B1-Motion>', self.draw_rect)
        self.selection_window.bind('<ButtonRelease-1>', self.end_rect)
        
        self.selection_window.wait_window()
        return "screenshot.png"
    
    def start_rect(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.current_rect:
            self.canvas.delete(self.current_rect)
        self.current_rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y, 
            outline='red', width=2
        )
    
    def draw_rect(self, event):
        if self.current_rect:
            self.canvas.coords(
                self.current_rect, 
                self.start_x, self.start_y, 
                event.x, event.y
            )
    
    def end_rect(self, event):
        x1 = min(self.start_x, event.x)
        y1 = min(self.start_y, event.y)
        x2 = max(self.start_x, event.x)
        y2 = max(self.start_y, event.y)
        
        self.selection_window.destroy()
        self.root.deiconify()
        
        self.root.after(100)
        screenshot = pyautogui.screenshot(region=(x1,y1,x2-x1, y2-y1))
        screenshot.save("screenshot.png")