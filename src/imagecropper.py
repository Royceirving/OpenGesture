import numpy as np
import cv2
import enum
import logging

logging.basicConfig(
    format="%(asctime)s [ImageCropper] [%(levelname)s] %(message)s",
    level=logging.INFO
)

class ImageCropper:

    class DrawingStates(enum.IntEnum):
        START = 0
        DRAWING = 1
        DONE_DRAWING = 2

    WINDOW_NAME = "Bounding Box Cropping"

    def __init__(self,image:np.ndarray) -> None:
        self.image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        self.image = image
        self.draw_image = image.copy()
        self.drawing_state = 0
        self.start_x = 0
        self.start_y = 0
        self.final_x = self.image.shape[0]
        self.final_y = self.image.shape[1]

    def _draw_crop_bounds_(self,event,x,y,flags,param):

        if(event == cv2.EVENT_LBUTTONDOWN):
            self.drawing_state = ImageCropper.DrawingStates.DRAWING
            self.start_x = x
            self.start_y = y
            logging.debug(f"Drawing started ({x},{y})")
        elif(event == cv2.EVENT_MOUSEMOVE and self.drawing_state == ImageCropper.DrawingStates.DRAWING):
            self.draw_image = self.image.copy()
            cv2.rectangle(self.draw_image,(self.start_x,self.start_y),(x,y), (0xFF,0,0), 2)
        elif(event == cv2.EVENT_LBUTTONUP and self.drawing_state == ImageCropper.DrawingStates.DRAWING):
            self.final_x = x
            self.final_y = y
            self.drawing_state = ImageCropper.DrawingStates.DONE_DRAWING

            logging.debug(f"Drawing Stopped ({x},{y})")


    def run(self) -> np.ndarray:
        cv2.namedWindow(ImageCropper.WINDOW_NAME)
        cv2.setMouseCallback(ImageCropper.WINDOW_NAME,self._draw_crop_bounds_)
        while(self.drawing_state < ImageCropper.DrawingStates.DONE_DRAWING):
            cv2.imshow(ImageCropper.WINDOW_NAME,self.draw_image)
            key_pressed = cv2.waitKey(20) & 0xFF
            # if esc, enter or space pressed
            if( key_pressed == 27 or key_pressed == 10 or key_pressed == 32):
                break
        cv2.destroyWindow(ImageCropper.WINDOW_NAME)
        if(self.drawing_state >= ImageCropper.DrawingStates.DONE_DRAWING):

            max_x = max(self.start_x,self.final_x)
            min_x = min(self.start_x,self.final_x)
            max_y = max(self.start_y,self.final_y)
            min_y = min(self.start_y,self.final_y)

            return self.image[min_y:max_y, min_x:max_x]
        else:
            return self.image
