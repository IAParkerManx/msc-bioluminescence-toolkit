import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

img1 = cv2.imread(r'C:\Users\Irshaad Parker\Downloads\vibrio plates\Test 18 April 2023\1.jpg')
img2 = cv2.imread(r'C:\Users\Irshaad Parker\Downloads\vibrio plates\Test 18 April 2023\2.jpg')

gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

blur = cv2.GaussianBlur(gray,(3,3), cv2.BORDER_DEFAULT)

canny = cv2.Canny(img1, 125, 175)
resizedImage = cv2.resize(canny, (0, 0), fx=0.25, fy=0.25)
cv2.imshow("resized", resizedImage)

cv2.waitKey(0)

kernel = np.ones((3, 3), np.uint8)
dilated_img2 = cv2.dilate(img2, kernel, iterations=1)

def plot_histogram(dilated_img2, title, mask = None):
    chans = cv2.split(dilated_img2)
    colors = ("b","g","r")
    plt.figure()
    plt.title(title)
    plt.xlabel("Bins")
    plt.ylabel("pixels")
    for (chan, colors) in zip(chans, colors):
        hist = cv2.calcHist([chan],[0], mask, [256], [0,256])
        plt.plot(hist, color = colors)
        plt.xlim([0,256])
plot_histogram(dilated_img2, "original", mask = None)
plt.show()

kernel = np.ones((3, 3), np.uint8)
dilated_img1 = cv2.dilate(img1, kernel, iterations=1)

kernel = np.ones((3, 3), np.uint8)
dilated_img2 = cv2.dilate(img2, kernel, iterations=1)





# Read the first image and convert it to LAB color space

lab1 = cv2.cvtColor(dilated_img1, cv2.COLOR_BGR2LAB)

# Initialize a list to store the mean square error values
mse_values = []

# Initialize a list to store the images with differences outlined
diff_images = []

lab2 = cv2.cvtColor(dilated_img2, cv2.COLOR_BGR2RGB)

    # Extract the blue-green channel
bg1 = lab1[:,:,1]
bg2 = lab2[:,:,1]

    # Apply adaptive thresholding to create a binary image
thresh1 = cv2.adaptiveThreshold(bg1, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
thresh2 = cv2.adaptiveThreshold(bg2, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    # Calculate the absolute difference between the two binary images
diff = cv2.absdiff(thresh1, thresh2)

    # Apply less blur to preserve edges
diff = cv2.GaussianBlur(diff, (3, 3), 0)

    # Find contours in the difference image
contours, hierarchy = cv2.findContours(diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw rectangles around the regions of differences on each image
img1_with_diff = dilated_img1.copy()
img2_with_diff = dilated_img2.copy()
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(img1_with_diff, (x, y), (x+w, y+h), (0, 0, 0), 1)
    cv2.rectangle(img2_with_diff, (x, y), (x+w, y+h), (0, 0, 0), 1)
diff_images.append(np.concatenate((img1_with_diff, img2_with_diff), axis=1))

    # Square the difference and take the mean to get the mean square error
mse = np.mean(diff ** 2)
mse_values.append(mse)
print(mse_values , mse)

    # Update the reference image for the next iteration
lab1 = lab2.copy()

# Calculate histogram without mask

hist1 = cv2.calcHist([img1_with_diff],[1],diff,[256],[0,256])
hist2 = cv2.calcHist([img2_with_diff],[1],diff,[256],[0,256])
hist3 = cv2.calcHist([img1],[1],diff,[256],[0,256])


plt.subplot(221), plt.imshow(img1_with_diff)
plt.subplot(222), plt.imshow(img2_with_diff)
plt.subplot(223), plt.imshow(diff)
plt.subplot(224), plt.plot(hist1), plt.plot(hist2),plt.plot(hist3)
plt.xlim([0,256])

plt.show()