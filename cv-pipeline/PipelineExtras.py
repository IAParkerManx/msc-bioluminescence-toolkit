

    # Append the difference between the control image and the processed image to the differences list
    diff0 = cv2.subtract(control_imge, img_copy)
    Gray1 = cv2.cvtColor(control_imge, cv2.COLOR_BGR2GRAY) #was 2GRAY
    Gray2 = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY) #was 2GRAY
    control_imge = img_copy
    (score0, diff2) = compare_ssim(Gray2, Gray1, win_size=3,gradient=False,dynamic_range=None, multichannel=True, gaussian_weights=None, full=True) ##Structural similarity algorithm
    diff_gray = cv2.cvtColor(diff0, cv2.COLOR_BGR2LAB)
    diff_mean = cv2.mean(diff_gray)[0]
    perc_change = score0
    differences_start.append(perc_change)
    differences_start1.append(perc_change)
    print("Similarity (SSIM) SCORE", perc_change)
    err = np.sum(diff0 ** 2)
    mse = err / float(height * width)
    msre = np.sqrt(mse)

    msedifferences_secondary.append(msre)

plt.plot(differences_start, label="SSIM")
plt.show()
plt.plot(differences_start1, label="SSIM")
plt.xlabel("Images per minute")
plt.ylabel("Similarity between control and treated samples")
plt.title('Image comparison')
plt.legend(loc="upper right")
plt.show()

plt.plot(msedifferences_secondary, label="rmse difference between original image")
plt.xlabel("Images")
plt.ylabel("Root mean square error")
plt.title('Root mean square error difference between images')
plt.legend(loc="upper right")
plt.show()
print(msedifferences_secondary)
max_diff_index1 = np.argmax(msedifferences_secondary)
print(max_diff_index1)
print(control_imge.shape)
print(img_copy.shape)
most_diff_image = cv2.imread(img_list[max_diff_index1-1])
print(most_diff_image.shape)


plt.show()
# Use t-test to determine if the differences between the control image and the other images are significant
#t_statistic, p_value = scipy.stats.ttest_ind(differences, [0] * len(differences))


# Use t-test to determine significance of differences
    #stat, p = scipy.stats.wilcoxon(differences, differences[0])


# Find the most different image
   # most_different_index = np.argmax(p)

# Compute the mean and standard deviation of the histograms
intensity_control = cv2.cvtColor(control_imge1, cv2.COLOR_BGR2LAB)
L, A, B = cv2.split(intensity_control)  # intensity L - LAB color space
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))

L_clahe = clahe.apply(L)
lab_clahe = cv2.merge((L_clahe, A, B))

intensity_img = cv2.cvtColor(img1, cv2.COLOR_BGR2LAB)
L, A, B = cv2.split(intensity_img)  # intensity L - LAB color space
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))

L_clahe = clahe.apply(L)
lab_clahe = cv2.merge((L_clahe, A, B))


intensity_most_diff = cv2.cvtColor(most_diff_image, cv2.COLOR_BGR2LAB)
L, A, B = cv2.split(intensity_most_diff)  # intensity L - LAB color space
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))

L_clahe = clahe.apply(L)
lab_clahe = cv2.merge((L_clahe, A, B))


print(intensity_control.shape)
print(intensity_img.shape)
print(intensity_most_diff.shape)

hist1 = cv2.calcHist([intensity_control],[0],None,[256],[0,256])


hist2 = cv2.calcHist([intensity_img],[0],None,[256],[0,256])


hist3 = cv2.calcHist(intensity_most_diff,[0],None,[256],[0,256])

plt.xlabel("Image comparison output")
plt.ylabel("Root mean square error")
plt.title('Root mean square error difference between images')
plt.subplot(221), plt.imshow(intensity_control, label="Control image intensity"), plt.title('Control image')

plt.subplot(222), plt.imshow(intensity_img, label="Final image intensity"), plt.title('Final image')
plt.subplot(223), plt.imshow(intensity_most_diff, label="Most different image"), plt.title('Most different image')
plt.subplot(224), plt.plot(hist1, label = "Control image"), plt.plot(hist2, label = "Final image"),plt.plot(hist3, label="Most different image"), plt.xlabel("Pixel value"), plt.ylabel("Pixel frequency"), plt.title('Intensities of images')
plt.xlim([0,256])
plt.legend()
plt.show()
max_diff_index = np.argmax(msedifferences_secondary)
print(max_diff_index)

mean_histogram1 = np.mean(hist1, axis=0)
print(mean_histogram1)
stddev_histogram1 = np.std(hist1, axis=0)
print(stddev_histogram1)
mean_histogram2 = np.mean(hist1, axis=0)
print(mean_histogram2)
stddev_histogram2 = np.std(hist1, axis=0)
print(stddev_histogram2)
mean_histogram3 = np.mean(hist1, axis=0)
print(mean_histogram3)
stddev_histogram3 = np.std(hist1, axis=0)
print(stddev_histogram3)

    # Plot the histogram with error bars
    #ax_hist = ax.twinx()
    #ax_hist.errorbar(np.arange(256), mean_histogram, yerr=stddev_histogram, fmt='.', capsize=1, color='r', alpha=0.5)
    #ax_hist.set_xlim([0, 256])
    #ax_hist.set_ylim([0, np.max(mean_histogram) + np.max(stddev_histogram)])
    #ax_hist.set_axis_off()

#plt.tight_layout()
#plt.show()

## outputs - Plot with control image, control image + contours, most different image + contours, histogram displaying channel 0 of LAB pictures (control + most different image)
## output - Plot with the SSIM of all images, and rmse of all images as error bars?

##Things to do: index the image with the highest SSIM difference. CalcHist for indexed image. Plot most different image with contours in the third window (should be the final image in the list)
##Need to determine how risk will be identified. Use SSIM differences to estimate risk
##Need to plot 4 concentrations (1x, 5x, 10x, 100x) for SSIM difference and rmse differences 6 points per 1 concentration for all images
##Need to plot error bars between each of the concentrations