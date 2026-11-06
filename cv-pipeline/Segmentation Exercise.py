import cv2
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats


# Load the image
img1 = cv2.imread(r'C:\Users\Irshaad Parker\Downloads\vibrio plates\test 0 pngs\20230322_121950.png')
img2 = cv2.imread(r'C:\Users\Irshaad Parker\Downloads\vibrio plates\test 0 pngs\20230322_121950.png')



gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)




ret, thresh1 = cv2.threshold(gray1, 140,180 , cv2.THRESH_BINARY+cv2.THRESH_OTSU)

res_thresh1 = cv2.resize(thresh1, None, fx= 0.25, fy = 0.25)
cv2.imshow('test', res_thresh1)

cv2.waitKey(0)


# Convert the images to grayscale
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)


# Compute the p-value using the Wilcoxon signed-rank test for each pixel
p_value = np.zeros_like(gray1, dtype=float)
for i in range(gray1.shape[0]):
    for j in range(gray1.shape[1]):
        data1 = gray1[i, j].astype(float).ravel()
        data2 = gray2[i, j].astype(float).ravel()
        p_value[i, j] = scipy.stats.wilcoxon(data1, data2)[1]

# Threshold the p-value to highlight regions of significant difference
thresh_p = cv2.threshold(p_value, 0.05, 1, cv2.THRESH_BINARY)[1]

# Dilate the thresholded p-value to enhance the regions of difference
kernel = np.ones((3, 3), np.uint8)
dilated = cv2.dilate(thresh_p, kernel, iterations=1)

# Overlay the dilated mask on the original image to highlight the regions of difference
overlay = img1.copy()
overlay[dilated == 1] = (0, 0, 255)

# Display the results
cv2.imshow('Image 1', img1)
cv2.imshow('Image 2', img2)
cv2.imshow('Thresholded Difference', dilated)
cv2.imshow('Overlay', overlay)
cv2.waitKey(0)
cv2.destroyAllWindows()
