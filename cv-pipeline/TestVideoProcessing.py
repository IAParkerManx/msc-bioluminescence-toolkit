import cv2
import numpy as np
import matplotlib.pyplot as plt

# Read the two videos
video1 = cv2.VideoCapture(r'C:\Users\Irshaad Parker\Pictures\Camera Roll\WIN_20230322_10_39_44_Pro.mp4')
video2 = cv2.VideoCapture(r'C:\Users\Irshaad Parker\Pictures\Camera Roll\WIN_20230322_10_48_39_Pro.mp4')

# Read the first frame of the videos
ret1, frame1 = video1.read()
ret2, frame2 = video2.read()

# Initialize the mean square error array
mse = []

while ret1 and ret2:
    # Convert frames to grayscale
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Create a blue color mask
    lower_blue = np.array([100, 0, 0])
    upper_blue = np.array([255, 50, 50])
    blue_mask = cv2.inRange(frame1, lower_blue, upper_blue)

    # Apply the mask to extract the blue pixels
    blue1 = cv2.bitwise_and(gray1, gray1, mask=blue_mask)
    blue2 = cv2.bitwise_and(gray2, gray2, mask=blue_mask)

    # Subtract the two blue frames
    diff = cv2.absdiff(blue1, blue2)

    # Calculate the mean square error of the difference
    err = np.mean((diff / 255) ** 2)
    mse.append(err)

    # Read the next frame
    ret1, frame1 = video1.read()
    ret2, frame2 = video2.read()

# Plot the mean square error
plt.plot(mse)
plt.title('Mean Square Error between Videos')
plt.xlabel('Frame')
plt.ylabel('MSE')
plt.show()
