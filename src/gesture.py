import cv2
import numpy as np
import matplotlib.pyplot as plt
import logging
import os

logging.basicConfig(
    format="%(asctime)s [Gesture] [%(levelname)s] %(message)s",
    level=logging.INFO
)

class Gesture:

    STRICT_DIST_MULT = 0.7
    RELAXED_DIST_MULT = 0.9
    PADDING = 5 # Pixels
    REQUIRED_GOOD_MATCHES = 2 # Number of strict matches before cropping
    DEFAULT_ACTIVATION_SCORE = 0.4

    def __init__(self, ground_truth_image) -> None:
        self.command = "echo \"No command specified\""
        sift = cv2.SIFT_create()
        self.gt_image = ground_truth_image
        self.gray_gt_image = cv2.cvtColor(self.gt_image,cv2.COLOR_BGR2GRAY)
        self.key_points_truth, self.descriptors_truth = sift.detectAndCompute(self.gray_gt_image,None)
        self._activation_score_ = Gesture.DEFAULT_ACTIVATION_SCORE
        logging.debug(f"{len(self.key_points_truth)} key points found for image")
        logging.debug("Key points and descriptors created for ground truth")
    #end __init__()

    # Fucntion to compare test image to the GT image and see if
    # the test image was a gesture
    def getLikeness(self,test_image,test_image_sift_pair):
        
        test_img_kp, test_img_desc = test_image_sift_pair
        sift = cv2.SIFT_create()
        matcher = cv2.BFMatcher()
        matches = matcher.knnMatch(self.descriptors_truth,test_img_desc,k=2)

        strict_good = []
        for m,n in matches:
            if m.distance < Gesture.STRICT_DIST_MULT*n.distance:
                strict_good.append([m])

        if(len(strict_good) > Gesture.REQUIRED_GOOD_MATCHES):
            center_kps = [test_img_kp[mat[0].trainIdx].pt for mat in strict_good]
            avg = np.average(center_kps,axis=0)
            avg = [int(v) for v in avg]

            x1 = int(max((avg[1] - (test_image.shape[0]/2 + Gesture.PADDING))   ,0))
            x2 = int(min((avg[1] + (test_image.shape[0]/2 + Gesture.PADDING))   ,test_image.shape[0]))
            y1 = int(max((avg[0] - (test_image.shape[1]/2 + Gesture.PADDING))   ,0))
            y2 = int(min((avg[0] + (test_image.shape[1]/2 + Gesture.PADDING))   ,test_image.shape[1]))
            sub_img = test_image[x1:x2,y1:y2]

            sub_kp, sub_desc = sift.detectAndCompute(sub_img,None)
            sub_matches = matcher.knnMatch(self.descriptors_truth,sub_desc,k=2)
            sub_good = []
            for m,n in sub_matches:
                if m.distance < Gesture.RELAXED_DIST_MULT*n.distance:
                    sub_good.append([m])

            # Ration of the padded cropped image key points match to the number of
            # descriptors in the ground truth image
            score = len(sub_good)/len(self.descriptors_truth)
            logging.debug("Confidence: {:.03f}".format(score))
            return score
        return 0
    #end getLikeness()

    # Checks if score is better than local activation score
    # Returns if command fired
    def check_and_trigger_command(self,score):
        if(score > self._activation_score_):
            logging.debug(self.command)
            os.system(self.command)
            return True
        return False
    #end check_and_trigger_command()

    def update_activation_score(self,score):
        self._activation_score_ = score
        logging.debug("Updated score to {}".format(self._activation_score_))
    #end update_activation_score()

#end class Gesture