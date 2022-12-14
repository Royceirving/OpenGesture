import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import os
import sys
import time
import logging

from addgesture import AddGesture
from showgestures import ShowGestures

#Threshold for number of matching features to consider a webcam image an image of a gesture
FEATURES_FOR_MATCH_THRESHOLD = 7

#Frame Number Delay between gesture register
DELAY_BETWEEN_GESTURES = 30

#Count of Rendered Frames
NUM_RENDERED_FRAMES = 0

#Number of times to check for gesture per second
NUM_CHECK_GESTURE_PER_SECOND = 5

MAX_FPS = 15

COUNTDOWN_TIME = 3 # seconds


logging.basicConfig(
    format="%(asctime)s [OpenGesture] [%(levelname)s] %(message)s",
    level=logging.DEBUG
)


class App:
    
    def __init__(self,capture_device:int = 0) -> None:
        self.window = tk.Tk()
        self.window.title("OpenGesture")
        self.window.resizable(width=None,height=None)
        
        self.label = tk.Label(self.window)
        self.label.grid(row=1,column=0)

        self.buttons_cell = tk.Frame(self.window,pady=5)
        self.buttons_cell.grid(row=0,column=0)


        self.add_gesture_btn = tk.Button(
            self.buttons_cell,
            text="Add Gesture",
            command=self._start_countdown_to_add_gesture_,
            padx=5
        )

        self.show_gesture_btn = tk.Button(
            self.buttons_cell,
            text="Show Gestures",
            command=self._show_gestures_,
            padx=5
        )

        self.add_gesture_btn.pack(side=tk.LEFT)
        self.show_gesture_btn.pack(side=tk.LEFT)

        self.capture_device = cv2.VideoCapture(capture_device)

        self.gestures = []
        self.last_activation = 0
        self.countdown_timer_end = None


    def _show_frame_(self):

        global NUM_RENDERED_FRAMES
        now = time.time()
        image = self._get_image_()

        tk_image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        tk_image = Image.fromarray(tk_image)
        tk_image = ImageTk.PhotoImage(image = tk_image)
        self.label.imgtk = tk_image
        self.label.configure(image=tk_image)

        self._update_countdown_timer_()
        
        if(NUM_RENDERED_FRAMES%NUM_CHECK_GESTURE_PER_SECOND == 0):
            if(NUM_RENDERED_FRAMES-self.last_activation > DELAY_BETWEEN_GESTURES):
                best = -1
                best_index = -1
                gesture_ct = 0
                for gesture in self.gestures:
                    num_features = gesture.getLikeness(image)
                    if(num_features > best):
                        best = num_features
                        best_index = gesture_ct
                    gesture_ct+=1
                if(best >= FEATURES_FOR_MATCH_THRESHOLD):
                    logging.debug(self.gestures[best_index].command)
                    self.last_activation = NUM_RENDERED_FRAMES
            
        # Check if image contains a gesture
        #adding a frame to rendered count
        NUM_RENDERED_FRAMES += 1

        self.label.after(int(1000/MAX_FPS),self._show_frame_)

    def _add_gesture_(self):
        gesture = AddGesture(self.window,self._get_image_()).run()
        self.gestures.append(gesture)

    def _show_gestures_(self):
        ShowGestures(self.window,self.gestures).run()

    def _start_countdown_to_add_gesture_(self):
        self.countdown_timer_end = time.time() + COUNTDOWN_TIME
    
    def _update_countdown_timer_(self):
        now = time.time()
        if(self.countdown_timer_end != None):
            self.add_gesture_btn.config(text=f"{int(self.countdown_timer_end-now)}")
            if(now > self.countdown_timer_end):
                self.countdown_timer_end = None
                self.add_gesture_btn.config(text="Add Gesture")
                logging.debug("Starting Add Gesture window")
                self._add_gesture_()

    def _get_image_(self,shape:tuple=None,gray:bool=False):
        good, image = self.capture_device.read()
        # Convert image to RGB
        if(gray):
            image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        else: #RGB
            # image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            pass
        #endif convert to grey or RGB
        
        if(type(shape) == tuple and len(shape) == 2):
            image = image.resize(shape)
        return image

    def run(self):
        self._show_frame_()
        self.window.mainloop()
