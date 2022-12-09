import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2


class AddGesture:

    def __init__(self,root_window,image) -> None:
        
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
        self.label.imgtk = image
        self.label.configure(image=image)
        

    def _submit_(self):
        
        """
        TODO: I think this is where we should add the model for our 
        CV work
        """
        # Text we got from the input box
        input_text = self.input_box.get()
        
        #Close current window
        self.window.destroy()

    def run(self):
        self.window.mainloop()