import cv2
import numpy as np


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


def get_mean_square_error(frame1, frame2):
    diff = cv2.absdiff(frame1, frame2)
    diff_squared = np.square(diff)
    mse = np.mean(diff_squared)
    return mse

# Open first video file and detect blue color regions
cap1 = cv2.VideoCapture(r'C:\Users\Irshaad Parker\Pictures\Camera Roll\WIN_20230322_10_39_44_Pro.mp4')
blue_regions1 = []
while True:
    ret, frame = cap1.read()
    if not ret:
        break
    blue_regions1.append(detect_blue(frame))

cap1.release()

# Open second video file and detect blue color regions
cap2 = cv2.VideoCapture(r'C:\Users\Irshaad Parker\Pictures\Camera Roll\WIN_20230322_10_48_39_Pro.mp4')
blue_regions2 = []
while True:
    ret, frame = cap2.read()
    if not ret:
        break
    blue_regions2.append(detect_blue(frame))

cap2.release()

# Subtract blue colored video from other and calculate mean square error
mses = []
for i in range(len(blue_regions1)):
    for j in range(len(blue_regions2)):
        diff = get_mean_square_error(blue_regions1[i], blue_regions2[j])
        mses.append(diff)

print('Mean square error values:', mses)
