import cv2
import numpy as np
import matplotlib.pyplot as plt

# Open the first video file
cap1 = cv2.VideoCapture(r'C:\Users\Irshaad Parker\Pictures\Camera Roll\WIN_20230322_10_39_44_Pro.mp4')

print(type(cap1))

# Open the second video file
cap2 = cv2.VideoCapture(r'C:\Users\Irshaad Parker\Pictures\Camera Roll\WIN_20230322_10_48_39_Pro.mp4')

# Get the frame rate of the videos
fps1 = cap1.get(cv2.CAP_PROP_FPS)
fps2 = cap2.get(cv2.CAP_PROP_FPS)

# Set the duration to 30 minutes
duration = 1 * 60

# Create a list to store the blue color changes for each video
blue_changes1 = []
blue_changes2 = []

# Get the first frame of each video
ret1, frame_prev1 = cap1.read()
ret2, frame_prev2 = cap2.read()

# Loop through the frames
frame_count = 0
while (cap1.isOpened() and cap2.isOpened()):
    # Check if the duration has passed
    if frame_count / fps1 > duration:
        break

    # Read the next frames
    ret1, frame_next1 = cap1.read()
    ret2, frame_next2 = cap2.read()

    # Check if the videos have ended
    if not ret1 or not ret2:
        break

    # Convert the frames to grayscale and blur them
    gray_prev1 = cv2.cvtColor(frame_prev1, cv2.COLOR_BGR2GRAY)
    gray_next1 = cv2.cvtColor(frame_next1, cv2.COLOR_BGR2GRAY)
    gray_prev2 = cv2.cvtColor(frame_prev2, cv2.COLOR_BGR2GRAY)
    gray_next2 = cv2.cvtColor(frame_next2, cv2.COLOR_BGR2GRAY)
    gray_prev1 = cv2.GaussianBlur(gray_prev1, (21, 21), 0)
    gray_next1 = cv2.GaussianBlur(gray_next1, (21, 21), 0)
    gray_prev2 = cv2.GaussianBlur(gray_prev2, (21, 21), 0)
    gray_next2 = cv2.GaussianBlur(gray_next2, (21, 21), 0)

    # Subtract the current frame from the previous frame
    frame_diff1 = cv2.absdiff(gray_prev1, gray_next1)
    frame_diff2 = cv2.absdiff(gray_prev2, gray_next2)

    print(frame_diff1)
    print(frame_diff2)

    # Apply a threshold to the difference image
    thresh1 = cv2.threshold(frame_diff1, 25, 255, cv2.THRESH_BINARY)[1]
    thresh2 = cv2.threshold(frame_diff2, 25, 255, cv2.THRESH_BINARY)[1]

    # Find the contours in the thresholded image
    contours1, hierarchy1 = cv2.findContours(thresh1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours2, hierarchy2 = cv2.findContours(thresh2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    # Loop through the contours
    blue_pixels1 = []
    blue_pixels2 = []
    for contour in contours1:
        # Get the area of the contour
        area = cv2.contourArea(contour)

        # If the area is too small, ignore the contour
        if area < 100:
            continue

            # Get the coordinates of the contour's bounding box
            x1, y1, w1, h1 = cv2.boundingRect(contour1)

# Find the index of the image with the highest difference


# Determine differences between the initial image and other images
differences_secondary = []
time_values = [1,2,3,4,5]

for folder_path in img_list[1:]:
    image = cv2.imread(folder_path)
    height = 4032
    width = 3024
    GrayA = cv2.cvtColor(control_imgd, cv2.COLOR_BGR2GRAY)
    GrayB = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (score, diff1) = compare_ssim(GrayA, GrayB, full=True)
    diff1 = (diff1 * 255).astype("uint8")
    difference = cv2.subtract(control_imgd, image)
    err = np.sum(diff1**2)
    mse = err/float(height*width)
    msre =np.sqrt(mse)
    differences_secondary.append(msre)
    print("SSIM: {}".format(score))
max_diff_index = np.argmax(differences_secondary)
print(max_diff_index)
plt.plot(differences_secondary)
plt.xlim(total_images)
plt.xlabel("Images")
plt.ylabel("Mean square error between images")
plt.title('Mean square error difference')
plt.show()