import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2

from addgesture import AddGesture

class App:
    
    def __init__(self,capture_device:int = 0) -> None:
        self.window = tk.Tk()
        self.window.title("OpenGesture")
        self.window.resizable(width=None,height=None)
        
        self.label = tk.Label(self.window)
        self.label.grid(row=1,column=0)

        self.btn = tk.Button(
            self.window,
            text="Add Gesture",
            command=self._add_gesture_
        )
        self.btn.grid(row=0,column=0)

        self.capture_device = cv2.VideoCapture(capture_device)

    def _show_frame_(self):
        tk_image = self._get_tk_image_()
        self.label.imgtk = tk_image
        self.label.configure(image=tk_image)
        self.label.after(int(1000/60),self._show_frame_)

    def _add_gesture_(self):
        AddGesture(self.window,self._get_tk_image_()).run()

    def _get_tk_image_(self):
        image = self.capture_device.read()
        # Convert image to RGB
        image = cv2.cvtColor(image[1],cv2.COLOR_BGR2RGB)
        # make an image?
        image = Image.fromarray(image)

        tk_image = ImageTk.PhotoImage(image = image)
        return tk_image

    def addGesture(self):
        pass

    def run(self):
        self._show_frame_()
        self.window.mainloop()
