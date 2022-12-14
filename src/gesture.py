import cv2
import numpy as np
import matplotlib.pyplot as plt
import logging

#Fast Library for Approximate Nearest Neighbors
#can be adjusted, came recommended
#need to probably figure out what each thing does
FLANN_INDEX_KDTREE = 1
FLANN_INDEX_PARAMS = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
FLANN_SEARCH_PARAMS = dict(checks=50)

#K Value for Number of Nearest Neighbors
#This should always be two rignt now, didn't code anything additional in
K_FOR_KNN = 2

#Lowes Ratio For Detecting How Similar Two Keypoints Are
LOWES_RATIO = 0.7

#Use FLANN Matcher (or BF Matcher)
USE_FLANN_MATCHER = True

logging.basicConfig(
    format="%(asctime)s [Gesture] [%(levelname)s] %(message)s",
    level=logging.DEBUG
)

printed = False


class Gesture:

    def __init__(self, ground_truth_image) -> None:
        self.command = "echo \"No command specified\""
        sift = cv2.SIFT_create()
        self.gt_image = ground_truth_image
        self.key_points_truth, self.descriptors_truth = sift.detectAndCompute(ground_truth_image,None)
        logging.debug(f"{len(self.key_points_truth)} key points found for image")
        # self.command = command #I NEED TO BE FORMATTED PLEASE AND THANK YOU DADDY
        logging.debug("Key points and descriptors created for ground truth")

    def show_key_points(self):
        kp_image = cv2.drawKeypoints(self.gt_image,self.key_points_truth,None)
        cv2.imshow("Ground Truth", kp_image)
        cv2.waitKey()

    # Fucntion to compare test image to the GT image and see if
    # the test image was a gesture
    def getLikeness(self,test_image):
        sub_image = test_image #temp may need to split the image
        sub_image_sift = cv2.SIFT_create()
        sub_image_kp, sub_image_desc = sub_image_sift.detectAndCompute(sub_image,None)

        if(USE_FLANN_MATCHER):
            # #Make FLANN based Matcher
            flann = cv2.FlannBasedMatcher(FLANN_INDEX_PARAMS,FLANN_SEARCH_PARAMS)
            matches = flann.knnMatch(self.descriptors_truth,sub_image_desc,k=K_FOR_KNN)
        else:
             #Make Brute Force Based Matcher
            bf = cv2.BFMatcher()
            matches = bf.knnMatch(self.descriptors_truth,sub_image_desc,k=2)

        positive_matches = []
        for match in matches:
            if match[0].distance < LOWES_RATIO*match[1].distance:
                positive_matches.append(match)

        return len(positive_matches) # a confidence value
