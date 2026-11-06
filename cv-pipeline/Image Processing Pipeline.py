#import libs

import cv2
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats
import os


#image acquisition

folder_path = r'C:\Users\Irshaad Parker\Downloads\vibrio plates\Latest samples'
image_files = sorted([os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.jpg')])

#image preprocessing

##Denoise


dst = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)

##histogram equalization

harris = cv2.cornerHarris(gray, 2, 3, 0.04)

img1[harris> 0.01*harris.max()] = [255,0,0]

##image normalization

eq_img = cv2.equalizeHist(img2)

#feature extraction
def detect_blue(img):
    # Convert image to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define blue color range
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([130, 255, 255])

    # Threshold the image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Find contours of blue regions
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Store blue color regions into a list
    blue_regions = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:
            x, y, w, h = cv2.boundingRect(contour)
            blue_regions.append((x, y, w, h))

    return blue_regions

##edge detection
canny = cv2.Canny(img1, 125, 175)

##segmentation

ret, thresh1 = cv2.threshold(eq_img, 140,180 , cv2.THRESH_BINARY+cv2.THRESH_OTSU)

res_thresh1 = cv2.resize(thresh1, None, fx= 0.25, fy = 0.25)
cv2.imshow('test', res_thresh1)

cv2.waitKey(0)

##contour identification

#classification
##determine differences between original and test image
