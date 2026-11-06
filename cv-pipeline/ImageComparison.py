import cv2
import numpy as np
import matplotlib.pyplot as plt

kernal = np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
img = []
image1 = cv2.resize(cv2.imread(r'C:\Users\Irshaad Parker\Downloads\vibrio plates\test 0\20230322_121950.jpg'), (300,300))
print(image1.shape)
image2 = cv2.resize(cv2.imread(r'C:\Users\Irshaad Parker\Downloads\vibrio plates\test 0\20230322_140117.jpg'), (300,300))
print(image2.shape)

mse = []

sharpened_image1 = cv2.filter2D(image1,-1,kernal)
sharpened_image2 = cv2.filter2D(image2,-1,kernal)


gray1 = cv2.cvtColor(sharpened_image1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(sharpened_image2, cv2.COLOR_BGR2GRAY)

lower_blue = np.array([50,50,50])
upper_blue = np.array([100,186,193])

blue_mask = cv2.inRange(image1, lower_blue, upper_blue)

blue1 = cv2.bitwise_and(gray1, gray1, mask=blue_mask)
blue2 = cv2.bitwise_and(gray2, gray2, mask=blue_mask)

contours, hierarchy = cv2.findContours(blue_mask,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(blue1, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # Calculate the center of the rectangle
    cx, cy = x + w // 2, y + h // 2
    # Get the center of the image
    rows, cols, _ = image1.shape
    center_x, center_y = cols // 2, rows // 2
    # Calculate the translation required to move the center of the rectangle to the center of the image
    tx, ty = center_x - cx, center_y - cy`
    # Apply the translation to the rectangle
    M = np.float32([[1, 0, tx], [0, 1, ty]])
    img = cv2.warpAffine(image1, M, (cols, rows))


resizedImage1 = cv2.resize(img, (0,0), fx = 0.5, fy = 0.5 )
cv2.imshow('resized', resizedImage1())
cv2.waitKey(0)



diff = cv2.absdiff(blue1, blue2)

err = np.mean((diff / 255) ** 2)
mse.append(err)

print(mse)
plt.plot(mse)
plt.title('Mean Square Error between Images')
plt.xlabel('Frame')
plt.ylabel('MSE')
plt.show()