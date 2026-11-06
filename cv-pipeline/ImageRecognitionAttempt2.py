import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

# Set the path to the folder containing the images
folder_path = r'C:\Users\Irshaad Parker\Downloads\vibrio plates\Latest samples'

# Get a list of all the image files in the folder
image_files = sorted([os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.jpg')])
for i in range(1, len(image_files)):
    reads = cv2.imread(image_files[i-1])
    sizes = reads.shape[:i]
    print(sizes)

# Initialize a list to store the images, differences, and MSE values
images = []
diffs = []
mse_values = []

# Loop over all the pairs of consecutive images and compare them
for i in range(1, len(image_files)):
    # Read the first and second images and convert them to LAB color space
    img1 = cv2.imread(image_files[i-1])
    img2 = cv2.imread(image_files[i])
    lab1 = cv2.cvtColor(img1, cv2.COLOR_BGR2LAB)
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
    diff = cv2.GaussianBlur(diff, (3, 3), 0)

    # Find contours in the difference image
    contours, hierarchy = cv2.findContours(diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw rectangles around the regions of differences on each image
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(img1, (x, y), (x+w, y+h), (0, 0, 255), 2)
        cv2.rectangle(img2, (x, y), (x+w, y+h), (0, 0, 255), 2)

    # Square the difference and take the mean to get the mean square error
    mse = np.mean(diff ** 2)
    mse_values.append(mse)

    # Update the reference image for the next iteration
    lab1 = lab2.copy()

    # Create a black image with the same size as the two input images
    height, width, channels = img1.shape
    diff_img = np.zeros((height, width, 3), dtype=np.uint8)

    # Draw red boxes around the regions of differences on the black image
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(diff_img, (x, y), (x+w, y+h), (0, 0, 255), 2)

    # Append the images and differences to their respective lists
    images.append(np.concatenate((img1, img2), axis=1))
    diffs.append(np.concatenate((diff_img, img2), axis=1))

# Concatenate all the images horizontally and vertically
all_images = np.concatenate(images, axis=0)
all_diffs = np.concatenate(diffs, axis =1)
output = np.concatenate((all_diffs, all_images), axis =0)


resized = cv2.resize(output, (0,0),fx = 0.1, fy =0.1)
# Display the image with regions of differences outlined
cv2.imshow('Comparison with Regions of Differences Outlined', resized)
cv2.waitKey(0)
cv2.destroyAllWindows()

time = np.arange(len(image_files)-1)
plt.plot(time, mse)
plt.xlabel('Time')
plt.ylabel('Mean Square Error')
plt.show()
# Print the mean square error
print('Mean Square Error:', mse)