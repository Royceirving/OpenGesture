import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np
import cv2
import logging

from gesture import Gesture
from imagecropper import ImageCropper

logging.basicConfig(
    format="%(asctime)s [AddGesture] [%(levelname)s] %(message)s",
    level=logging.DEBUG
)



class AddGesture:

    def __init__(self,root_window,image) -> None:

        cropped_image = ImageCropper(image=image).run()
        self.gesture = Gesture(cropped_image)

        self.window = tk.Toplevel(root_window)
        self.window.resizable(width=None,height=None)
        self.window.title("Add Gesture")

        # Frame to wrap all text entry into a nice box
        self.cell = tk.Frame(self.window)
        self.cell.grid(row=0,column=0)

        self.text_box = tk.Label(
            self.cell,
            text="Command:"
        )

        self.input_box = tk.Entry(
            self.cell
        )
        self.input_box.focus_get()

        self.submit_btn = tk.Button(
            self.cell,
            text="Submit",
            command=self._submit_
        )

        # Pack everything into the frame
        self.text_box.pack(side=tk.LEFT)
        self.input_box.pack(side=tk.LEFT)
        self.submit_btn.pack(side=tk.LEFT)

        # Show image that we captured
        self.label = tk.Label(self.window)
        self.label.grid(row=1,column=0)
        tk_image = cv2.cvtColor(cropped_image,cv2.COLOR_BGR2RGB)
        tk_image = Image.fromarray(tk_image)
        tk_image = ImageTk.PhotoImage(image = tk_image)
        self.label.imgtk = tk_image
        self.label.configure(image=tk_image)

        

    def _submit_(self):
        
        """
        TODO: I think this is where we should add the model for our 
        CV work
        """
        # self.gesture.show_key_points()
        # Text we got from the input box
        self.gesture.command = self.input_box.get()
        #Close current window
        self.window.destroy()
        self.window.quit()

    def run(self):
        self.window.mainloop()
        logging.debug("Returning gesture")
        return self.gesture