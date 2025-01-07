import tkinter as tk 
import pyautogui
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os

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

    def overlay_translations(self, image_path: str, translations: list) -> str:
        try:
            image = Image.open(image_path)
            draw = ImageDraw.Draw(image)
            
            for text_block, translated_text in translations:
                left, top, width, height = text_block.position

                # cria um retângulo branco sobre o texto original
                overlay = Image.new('RGBA', (width, height), (255, 255, 255, 180))
                image.paste(overlay, (left, top), overlay)

                font = self.get_font_size(translated_text, width, height)

                #pega as dimensões do texto
                bbox = font.getbbox(translated_text)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

                #centraliza o texto no retangulo
                text_x = left + (width - text_width) // 2
                text_y = top + (height - text_height) // 2

                draw.text((text_x, text_y), translated_text, font=font, fill='black')
            
            output_path = "translated_screenshot.png"
            image.save(output_path)
            os.startfile(output_path)

            return output_path

        except Exception as e:
            print(f"Erro ao sobrepor traduções: {e}")
            return image_path
        
    def get_font_size(self, text, max_width, max_height):
        font_size = 12
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
            return font
        
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        if text_width > max_width:
            font_size = int(font_size * (max_width / text_width) * 0.9)
        
        if text_height > max_height:
            font_size = int(font_size * (max_height / text_height) * 0.9)
        
        try: 
            return ImageFont.truetype("arial.ttf", font_size)
        except:
            return ImageFont.load_default()
        
            