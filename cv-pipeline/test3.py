import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

# Set the path to the folder containing the images
folder_path = r'C:\Users\Irshaad Parker\Downloads\vibrio plates\Latest samples'

# Get a list of all the image files in the folder
image_files = sorted([os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.jpg')])

# Read the first image and convert it to LAB color space
img1 = cv2.imread(image_files[0])
lab1 = cv2.cvtColor(img1, cv2.COLOR_BGR2LAB)

# Initialize a list to store the mean square error values
mse_values = []

# Initialize a list to store the images with differences outlined
diff_images = []

# Loop over all the pairs of consecutive images and compare them
for i in range(1, len(image_files)):
    # Read the second image and convert it to LAB color space
    img2 = cv2.imread(image_files[i])

    lab2 = cv2.cvtColor(img2, cv2.COLOR_BGR2LAB)

    # Extract the blue-green channel
    bg1 = lab1[:,:,1]
    bg2 = lab2[:,:,1]

    # Apply adaptive thresholding to create a binary image
    thresh1 = cv2.adaptiveThreshold(bg1, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    thresh2 = cv2.adaptiveThreshold(bg2, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    # Calculate the absolute difference between the two binary images
    diff = cv2.absdiff(thresh1, thresh2)

    # Apply less blur to preserve edges
    diff = cv2.GaussianBlur(diff, (5, 5), 1)

    # Find contours in the difference image
    contours, hierarchy = cv2.findContours(diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw rectangles around the regions of differences on each image
    img1_with_diff = img1.copy()
    img2_with_diff = img2.copy()
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(img1_with_diff, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(img2_with_diff, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # Append the images with differences outlined to the list
    diff_images.append(np.concatenate((img1_with_diff, img2_with_diff), axis=1))


    # Square the difference and take the mean to get the mean square error
    mse = np.mean(diff ** 2)
    mse_values.append(mse)

    # Update the reference image for the next iteration
    lab1 = lab2.copy()
print(diff)
# Concatenate all the images horizontally
all_images = img1.copy()
for i in range(len(diff_images)):
    all_images = np.concatenate((all_images, diff_images[i]), axis=1)


resize = cv2.resize(all_images, (0,0), fx = 0.1, fy = 0.1)
cv2.imshow('all images', resize)
cv2.waitKey(0)
print(mse)
# Concatenate the mean square error plot vertically
plt.plot(mse_values)
plt.savefig('mse_plot.png')
mse_plot = cv2.imread('mse_plot.png')


for i in all_images :

    hist1 = cv2.calcHist([img1_with_diff],[0],diff,[256],[0,256])
    hist2 = cv2.calcHist([img2_with_diff],[1],diff,[256],[0,256])
    hist3 = cv2.calcHist([img1],[2],diff,[256],[0,256])

    plt.subplot(221), plt.imshow(img2_with_diff)
    plt.subplot(222), plt.imshow(img1_with_diff)
    plt.subplot(223), plt.imshow(diff)
    plt.subplot(224), plt.plot(hist1), plt.plot(hist2),plt.plot(hist3)
    plt.xlim([0,256])


    plt.show()