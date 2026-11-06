import cv2
import numpy as np
import glob as glob
import matplotlib.pyplot as plt
import argparse
import matplotlib.image as mpimg

img =[]
M = []
kernal = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])

image1 = cv2.imread(r'C:\Users\Irshaad Parker\Downloads\vibrio plates\Latest samples\20230327_135425.jpg')
print(image1.shape)
##image2 = cv2.resize(cv2.imread(r'C:\Users\Irshaad Parker\Downloads\vibrio plates\test 0 pngs\20230322_140117.png'), (300,300))
##print(image2.shape)
##image1 = mpimg.imread(r'C:\Users\Irshaad Parker\Downloads\testimage6.jpeg')
##imgplot = plt.imshow(image1)
##plt.show()

##colour to gray
##image2 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)

##edge detection
cv2.imwrite('edges_plate.jpg', cv2.Canny(image1,100, 200))
cv2.imshow('edges', cv2.imread('edges_plate.jpg'))
cv2.waitKey(0)

## sharpen and convert to hsv
##sharpened_image = cv2.filter2D(image1, -1, kernal)

print(type(hsv))

##blue bounds selects a region within the blue bounds retrieved from imageJ
##current ranges isolates ROI aka region of interest

lower_blue = np.array([10, 10, 15])
upper_blue = np.array([137, 159, 28])

hsv = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, lower_blue, upper_blue)
result = cv2.bitwise_and(image1, image1, mask=mask)

## finding contours and framing the colours in green boxes
contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
##bouding the contours to boxes
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # Calculate the center of the rectangle
    cx, cy = x + w // 2, y + h // 2
    # Get the center of the image
    rows, cols, _= image1.shape
    center_x, center_y = cols // 2, rows // 2
    # Calculate the translation required to move the center of the rectangle to the center of the image
    tx, ty = center_x - cx, center_y - cy
    # Apply the translation to the rectangle
    M = np.float32([[1, 0, tx], [0, 1, ty]])
    img = cv2.warpAffine(image1, M, (cols, rows))

resizedImage1 = cv2.resize(img, (0, 0), fx=0.1, fy=0.1)


cv2.imshow('resized', resizedImage1)
cv2.waitKey(0)
print('done')
print(type(M))


# Show the image with the rectangles

##imgplot = plt.imshow(img)
##plt.show()



##extract the region of interest


##displaying contours on original image


##cv2.imshow('Final Image', image1)
##cv2.waitKey(0)

cv2.imshow('Mask', mask )
cv2.waitKey(0)
cv2.imshow('MaskedImage', result)
cv2.waitKey(0)


assert image1 is not None, "file could not be read, check with os.path.exists()"
