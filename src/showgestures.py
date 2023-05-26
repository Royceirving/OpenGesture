import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import logging

logging.basicConfig(
    format="%(asctime)s [ShowGestures] [%(levelname)s] %(message)s",
    level=logging.INFO
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
            
            text_box = tk.Label(
                self.window,
                text = gesture.command,
            )
            text_box.grid(row=y,column=x)

            label = tk.Label(self.window)
            label.grid(row=y+1,column=x)
            tk_image = cv2.cvtColor(gesture.gt_image,cv2.COLOR_BGR2RGB)
            tk_image = Image.fromarray(tk_image)
            tk_image = ImageTk.PhotoImage(image = tk_image)
            label.imgtk = tk_image
            label.configure(image=tk_image)


            threshold_cell = tk.Frame(self.window)
            threshold_cell.grid(row=y+2,column=x)

            update_activation_text = tk.Label(
                threshold_cell,
                text="Activation Score:"
            )

            input_box = tk.Entry(
                threshold_cell
            )
            input_box.insert(0,str(gesture._activation_score_))

            update_btn = tk.Button(
                threshold_cell,
                text="Update",
                command=lambda: gesture.update_activation_score(min(max(float(input_box.get()),0.0),1.0))
            )
            update_activation_text.pack(side=tk.LEFT)
            input_box.pack(side=tk.LEFT)
            update_btn.pack(side=tk.LEFT)

            x = x+1
            if(x >= ShowGestures.GESTURES_PER_ROW):
                y += 3
                x = 0
            #end updating new row update
        #end iterating through the list of gestures
    #end __init__()

    def run(self):
        self.window.mainloop()
    #end run()
#end class ShowGestures