import cv2
import numpy as np
import argparse, sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from sklearn.cluster import KMeans
from sklearn import linear_model


NUM_COLORS = 3

CENTERS = [[0, 0, 0], [0, 255, 255], [255, 255, 255]] 

np.random.seed(5)

IMG_PATH = '''IMG PATH'''

cv_img = cv2.imread("strip.jpg")
# print cv_img.shape

# class GetKMeansModel(object):
# 	def __init__(self, img)
def getimgdatapts(cv2img):
	x, y, p = cv2img.shape
	data = []
	# print x, y
	for i in range(x):
		for j in range(y):
			# print cv2img[i][j]
			data.append(cv2img[i][j])
	npdata = np.asarray(data)
	# print npdata.shape
	# print npdata[1]

	return npdata

#priors
def runKMeans():
	testdata = getimgdatapts(cv_img)
	kmc = KMeans(n_clusters = NUM_COLORS, max_iter = 100)
	kmc.fit(testdata)
	trained_centers = kmc.cluster_centers_
	# print trained_centers
	# print CENTERS
	return trained_centers


def identifyColors(trained, true):
	numcolors, _ = trained.shape
	# print numcolors
	matching = np.zeros((numcolors, numcolors))
	# print matching
	for i, color in enumerate(trained):
		# print color
		for j, truecolor in enumerate(true):
			matching[i][j] = np.linalg.norm(color - truecolor)

	# print matching
	colormap= {}
	for i, color in enumerate(matching):
		colormap[i] = np.argmin(color)
		# print colormap
	return colormap

def getparameters(mapping, trained, true):
	redX = []
	redY = []
	greenX = []
	greenY = []
	blueX = []
	blueY = []
	# print type(redY), redX
	for i, color in enumerate(true):
		mapped = mapping[i]
		# print i, color
		for j, index in enumerate(color):
			# print index
			if j == 0:
				redX.append(index)
			if j == 1:
				greenX.append(index)
			if j == 2:
				blueX.append(index)
		for j2, index2 in enumerate(trained[mapped]):
			# print j2, index2
			if j2 == 0:
				redY.append(index2)
			if j2 == 1:
				greenY.append(index2)
			if j2 == 2:
				blueY.append(index2)
	# print redX
	np.asarray(redX).T
	np.asarray(redY).T
	np.asarray(greenX).T
	np.asarray(greenY).T
	np.asarray(blueX).T
	np.asarray(blueY).T
	print type(redY), redX
	RED = linear_model.LinearRegression()
	BLUE = linear_model.LinearRegression()
	GREEN = linear_model.LinearRegression()
	RED.fit(redX, redY)
	BLUE.fit(blueX, blueY)
	GREEN.fit(greenX, greenY)
	print RED.coef_, RED.intercept_
	print BLUE.coef_, BLUE.intercept_
	print GREEN.coef_, GREEN.intercept_





trained = runKMeans()
mapping = identifyColors(trained, CENTERS)
getparameters(mapping, trained, CENTERS)
