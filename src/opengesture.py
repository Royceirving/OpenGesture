import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from numpy import zeros, ndarray
import cv2
import time
import logging

from addgesture import AddGesture
from showgestures import ShowGestures
from gestureloader import GestureLoadManager

#Frame Number Delay between gesture register
DELAY_BETWEEN_GESTURES = 30

#Count of Rendered Frames
NUM_RENDERED_FRAMES = 0

#Number of times to check for gesture per second
NUM_CHECK_GESTURE_PER_SECOND = 5

MAX_FPS = 60

COUNTDOWN_TIME = 3 # seconds

logging.basicConfig(
    format="%(asctime)s [OpenGesture] [%(levelname)s] %(message)s",
    level=logging.INFO
)

class OpenGesture:
    
    def __init__(self,capture_device:int = 0,verbose=False) -> None:

        self.capture_device = cv2.VideoCapture(capture_device) # Camera device

        self.gestures = [] # List of gestures that we have saved
        self.last_activation = 0 # Last time we activated a gesture command
        self.countdown_timer_end = None # time for add gesture timer
        self.show_features = False
        self._show_video_ = True
        self.last_frame_timestamp = time.time()


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

        # self.save_btn = tk.Button(
        #     self.buttons_cell,
        #     text="Save",
        #     command=self._save_gestures_,
        #     padx=5
        # )

        # self.load_btn = tk.Button(
        #     self.buttons_cell,
        #     text="Load",
        #     command=self._load_gestures_,
        #     padx=5
        # )

        self.add_gesture_btn.pack(side=tk.LEFT)
        self.show_gesture_btn.pack(side=tk.LEFT)
        # self.load_btn.pack(side=tk.LEFT)
        # self.save_btn.pack(side=tk.LEFT)


        # BEGIN SECTION SideBar        
        self.side_bar = tk.Frame(self.window)
        self.side_bar.grid(row=1,column=1)

        self.show_features_btn = tk.Button(
            self.side_bar,
            text="Toggle Features",
            command=self._toggle_show_features_
        )
        self.show_features_btn.pack(side=tk.TOP)

        self.show_video_btn = tk.Button(
            self.side_bar,
            text="Toggle Video",
            command=self._toggle_show_video_
        )
        self.show_video_btn.pack(side=tk.TOP)

        #END SECTION SideBar

        self.frame_delay_text = tk.Label(
            self.window,
            text="Frame delay: 0.000ms"
        )
        self.frame_delay_text.grid(row=2,column=1)

        
        self.loaded_gestures_text = tk.Label(
            self.window,
            text="Loaded Gestures: 0"
        )
        self.loaded_gestures_text.grid(row=2,column=0)
    #end init

    def _update_(self):

        image = self._get_image_()
        now = time.time()
        self.frame_delay_text.configure(text="Frame delay: {:.3f}ms".format(
            ((now - self.last_frame_timestamp) - (1/MAX_FPS))
        ))
        self.last_frame_timestamp = now

        sift = cv2.SIFT_create()
        gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        test_image_sift_pair = sift.detectAndCompute(gray_image,None)

        self._check_gestures_(gray_image,test_image_sift_pair)

        if(self._show_video_):
            if(self.show_features):
                image = cv2.drawKeypoints(
                    image=gray_image,
                    keypoints=test_image_sift_pair[0],
                    outImage=image
                )

            tk_image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            tk_image = Image.fromarray(tk_image)
            tk_image = ImageTk.PhotoImage(image = tk_image)
            self.label.imgtk = tk_image
            self.label.configure(image=tk_image)

        self.loaded_gestures_text.config(text=f"Loaded Gestures: {len(self.gestures)}")

        self.label.after(int(1000/MAX_FPS),self._update_)
    #end _update_()

    def _check_gestures_(self,test_image,test_image_sift_pair):
        global NUM_RENDERED_FRAMES
        # Check if image contains a gesture       
        if(NUM_RENDERED_FRAMES%NUM_CHECK_GESTURE_PER_SECOND == 0 and not self._update_countdown_timer_()):
            if(NUM_RENDERED_FRAMES-self.last_activation > DELAY_BETWEEN_GESTURES):
                best = -1
                best_index = -1
                gesture_ct = 0
                for gesture in self.gestures:
                    num_features = gesture.getLikeness(test_image,test_image_sift_pair)
                    if(num_features > best):
                        best = num_features
                        best_index = gesture_ct
                    gesture_ct+=1
                if(best_index >= 0 and self.gestures[best_index].check_and_trigger_command(best)):
                    logging.debug(f"{best:.03f} Gesture Activated")
                    self.last_activation = NUM_RENDERED_FRAMES

        #adding a frame to rendered count
        NUM_RENDERED_FRAMES += 1
    #end _check_gestures_()

    def _add_gesture_(self):
        gesture = AddGesture(self.window,self._get_image_()).run()
        self.gestures.append(gesture)
        return True
    # end _add_gesture_()

    def _show_gestures_(self):
        ShowGestures(self.window,self.gestures).run()
    #end _show_gestures_()

    def _start_countdown_to_add_gesture_(self):
        self.countdown_timer_end = time.time() + COUNTDOWN_TIME
    #end _start_countdown_to_add_gesture_()

    def _update_countdown_timer_(self):
        now = time.time()
        if(self.countdown_timer_end != None):
            self.add_gesture_btn.config(text=f"{int(self.countdown_timer_end-now)}")
            if(now > self.countdown_timer_end):
                self.countdown_timer_end = None
                self.add_gesture_btn.config(text="Add Gesture")
                logging.debug("Starting Add Gesture window")
                return self._add_gesture_()
            #end timer activation
        #end timer check and button update check
        return False
    #end _update_countdown_timer_()

    def _get_image_(self,shape:tuple=None):
        good, image = self.capture_device.read()
        if(not good):
            logging.error("Error reading image from capture device")
            return zeros((0))
        #endif valid caputre of image
        if(type(shape) == tuple and len(shape) == 2):
            image = image.resize(shape)
        return image
    #end _get_image_()

    def _save_gestures_(self):
        GestureLoadManager.save(self.gestures)
    #end _save_gestures_()

    def _load_gestures_(self):
        self.gestures = GestureLoadManager.load()
    #end _load_gestures_()

    def _toggle_show_features_(self):
        self.show_features = not self.show_features
    #end _toggle_show_features_()

    def _toggle_show_video_(self):
        self._show_video_ = not self._show_video_
    #end _toggle_show_video_

    def run(self):
        try:
            self._update_()
            self.window.mainloop()
        except KeyboardInterrupt:
            self.window.destroy()
    #end run()
#end OpenGesture