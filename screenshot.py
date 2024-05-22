import tkinter as tk
import pyautogui
import datetime
import os

class SnippingApp:
    def __init__(self):
        self.start_x = self.start_y = self.end_x = self.end_y = 0
        self.snipping_frame = tk.Tk()
        self.snipping_frame.withdraw()  # Hide the main window
        self.start_snip()

    def start_snip(self):
        self.snipping_frame = tk.Tk()
        self.snipping_frame.attributes('-fullscreen', True)
        self.snipping_frame.attributes('-alpha', 0.3)  # Semi-transparent
        self.snipping_frame.overrideredirect(True)  # Remove window decorations

        self.canvas = tk.Canvas(self.snipping_frame, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)
        self.canvas.bind('<ButtonPress-1>', self.on_button_press)
        self.canvas.bind('<B1-Motion>', self.on_move_press)
        self.canvas.bind('<ButtonRelease-1>', self.on_button_release)

    def on_button_press(self, event):
        self.start_x = self.snipping_frame.winfo_pointerx() - self.snipping_frame.winfo_rootx()
        self.start_y = self.snipping_frame.winfo_pointery() - self.snipping_frame.winfo_rooty()
        self.canvas.delete("rect")

    def on_move_press(self, event):
        cur_x = self.snipping_frame.winfo_pointerx() - self.snipping_frame.winfo_rootx()
        cur_y = self.snipping_frame.winfo_pointery() - self.snipping_frame.winfo_rooty()
        self.canvas.delete("rect")
        self.canvas.create_rectangle(self.start_x, self.start_y, cur_x, cur_y, outline="white", width=2, tags="rect")

    def on_button_release(self, event):
        self.end_x = self.snipping_frame.winfo_pointerx() - self.snipping_frame.winfo_rootx()
        self.end_y = self.snipping_frame.winfo_pointery() - self.snipping_frame.winfo_rooty()
        self.snipping_frame.withdraw()  # Hide the snipping frame

        if self.end_x > self.start_x and self.end_y > self.start_y:
            take_bounded_screenshot(self.start_x, self.start_y, self.end_x, self.end_y)

def take_bounded_screenshot(x1, y1, x2, y2):
    if not os.path.exists("snips"):
        os.makedirs("snips")

    image = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    file_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".png"
    image.save(os.path.join("snips", file_name))

if __name__ == "__main__":
    app = SnippingApp()
    tk.mainloop()
