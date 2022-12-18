import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np
import cv2
import logging

from gesture import Gesture

logging.basicConfig(
    format="%(asctime)s [ShowGestures] [%(levelname)s] %(message)s",
    level=logging.DEBUG
)

class ShowGestures:

    GESTURES_PER_ROW = 3

    def __init__(self,root_window,gestures_list):

        self.window = tk.Toplevel(root_window)
        self.window.resizable(width=None,height=None)
        self.window.title("Gestures")

        x = 0
        y = 0
        for gesture in gestures_list:
            
            self.text_box = tk.Label(
                self.window,
                text = gesture.command
            )
            self.text_box.grid(row=y+1,column=x)

            self.label = tk.Label(self.window)
            self.label.grid(row=y,column=x)
            tk_image = cv2.cvtColor(gesture.gt_image,cv2.COLOR_BGR2RGB)
            tk_image = Image.fromarray(tk_image)
            tk_image = ImageTk.PhotoImage(image = tk_image)
            self.label.imgtk = tk_image
            self.label.configure(image=tk_image)

            x = x+1
            if(x >= ShowGestures.GESTURES_PER_ROW):
                y += 2
                x = 0

    def run(self):
        self.window.mainloop()