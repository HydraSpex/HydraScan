#Maxima Detection

# import the necessary packages
from scipy import ndimage as ndi
import scipy.ndimage.filters as filters
import matplotlib.pyplot as plt
import numpy as np

def Maxima_Detection_Threshold(data, low, dist=5):
		#Numpy Array erzeugen
		x = data
		im = np.array([np.array(xi) for xi in x])
		image = np.array([np.array(xi) for xi in x])

		data_max = filters.maximum_filter(im, dist)
		maxima = (im == data_max)
		data_min = filters.minimum_filter(im, dist)
		diff = ((data_max - data_min) > low)
		maxima[diff == 0] = 0

		labeled, num_objects = ndi.label(maxima)
		slices = ndi.find_objects(labeled)
		x, y = [], []
		for dy,dx in slices:
				x_center = (dx.start + dx.stop - 1)/2
				x.append(x_center)
				y_center = (dy.start + dy.stop - 1)/2    
				y.append(y_center)

		coordinatesNew = list()
		i = 0
		while i < len(x):
				coordinatesLine = list()
				coordinatesLine.append(y[i])
				coordinatesLine.append(x[i])
				coordinatesNew.append(coordinatesLine)
				i += 1

		x = coordinatesNew
		coordinates = np.array([np.array(xi) for xi in x])

		return image, im, coordinates, low


def Maxima_Detection_NumMax(data, num_max, dist):
		#Numpy Array erzeugen
		x = data
		image = np.array([np.array(xi) for xi in x])
		image_th = np.array([np.array(xi) for xi in x])
		image_th_old = np.array([np.array(xi) for xi in x])

		low = 0
		x = []
		while len(x) > num_max or len(x) == 0:
				data_max = filters.maximum_filter(image_th, dist)
				maxima = (image_th == data_max)
				data_min = filters.minimum_filter(image_th, dist)
				diff = ((data_max - data_min) > low)
				maxima[diff == 0] = 0

				labeled, num_objects = ndi.label(maxima)
				slices = ndi.find_objects(labeled)
				x, y = [], []
				for dy,dx in slices:
						x_center = (dx.start + dx.stop - 1)/2
						x.append(x_center)
						y_center = (dy.start + dy.stop - 1)/2    
						y.append(y_center)

				low_old = low
				length_old = len(x)

				low += 0.5

				if len(x) == 0:
						break

		if len(x) < num_max:
				print("Could only find " + str(len(x)) + " or " + str(length_old))
				if (abs(num_max - len(x)) > abs(num_max - length_old)):
						low = low_old-0.05
						print("Choose " + str(length_old) + " with " + str(low) + " Threshold")
						data_max = filters.maximum_filter(image_th_old, dist)
						maxima = (image_th_old == data_max)
						data_min = filters.minimum_filter(image_th_old, dist)
						diff = ((data_max - data_min) > low)
						maxima[diff == 0] = 0

						labeled, num_objects = ndi.label(maxima)
						slices = ndi.find_objects(labeled)
						x, y = [], []
						for dy,dx in slices:
								x_center = (dx.start + dx.stop - 1)/2
								x.append(x_center)
								y_center = (dy.start + dy.stop - 1)/2    
								y.append(y_center)
						image_show = image_th_old
				else:
						print("Choose " + str(len(x)) + " with " + str(low) + " Threshold")
						image_show = image_th
		else:
				print("Found " + str(len(x)))
				image_show = image_th



		coordinatesNew = list()
		i = 0
		while i < len(x):
				coordinatesLine = list()
				coordinatesLine.append(y[i])
				coordinatesLine.append(x[i])
				coordinatesNew.append(coordinatesLine)
				i += 1

		x = coordinatesNew
		coordinates = np.array([np.array(xi) for xi in x])
		#Plot_Maxima(image, image_show, coordinates, low)
		
		return image, image_show, coordinates, low

def Plot_Maxima(image, image_show, coordinates, low):
		#Image Maxima Filter
		image_max = ndi.maximum_filter(image_show, size=5, mode='constant')

		#Show results
		fig, axes = plt.subplots(1, 3, figsize=(8, 3), sharex=True, sharey=True)
		ax = axes.ravel()
		ax[0].imshow(image, cmap=plt.cm.gray)
		ax[0].axis('off')
		ax[0].set_title('Original')

		"""
		if (abs(num_max - len(coordinates)) > abs(num_max - length_old)):
				name = "Threshold filter: " + str(low_old)
				ax[1].imshow(image_th_old, cmap=plt.cm.gray)
		else:
				name = "Threshold filter: " + str(low)
				ax[1].imshow(image_th, cmap=plt.cm.gray)
		"""

		name = "Threshold filter: " + str(low)
		ax[1].imshow(image_show, cmap=plt.cm.gray)
		ax[1].axis('off')
		ax[1].set_title(name)

		"""
		ax[2].imshow(image_max, cmap=plt.cm.gray)
		ax[2].axis('off')
		ax[2].set_title('Maximum filter')
		"""

		name = "LocalMax with " + str(len(coordinates)) + " Maxima"
		ax[2].imshow(image, cmap=plt.cm.gray)
		ax[2].autoscale(False)
		ax[2].plot(coordinates[:, 1], coordinates[:, 0], color='#9dea54ff', marker='x', markersize=10, linestyle='none')
		ax[2].axis('off')
		ax[2].set_title(name)

		fig.tight_layout()

		plt.show()
