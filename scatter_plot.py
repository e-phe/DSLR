#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import re
import sys

def scatterPlot(data, features):
	plt.xlabel(data[0, features[0]])
	plt.ylabel(data[0, features[1]])
	plt.scatter(data[1:, features[0]].astype(float), data[1:, features[1]].astype(float))
	plt.show()

def similarFeatures(data):
	longest = 0
	features = []
	for i in range(0, len(data[0])):
		for j in range(i + 1, len(data[0])):
			similarities = len(set(data[1:, i]) & set(data[1:, j]))
			if longest < similarities:
				longest = similarities
				features = [i, j]
	return features

def prepData(data):
	for i in range(0, len(data[0])):
		for j in range(1, len(data)):
			data[j, i] = str(abs(float(data[j, i]))).replace('.', '')
	return data

def delCoLette(data, i):
	for j in range(1, len(data)):
		if data[j, i] != str(np.nan) and re.search("^[+-]?([0-9]+[.])?[0-9]+$", data[j, i]) == None:
			return [np.delete(data, i, 1), i]
	return [data, i + 1]

if __name__ == "__main__":
	try:
		data = np.loadtxt("datasets/dataset_train.csv", dtype = str, delimiter = ",")
	except:
		sys.exit("Error")
	data = np.delete(data, 0, 1)
	data[data == ''] = np.nan
	i = 0
	while i < len(data[0]):
		[data, i] = delCoLette(data, i)
	features = similarFeatures(prepData(data.copy()))
	scatterPlot(data, features)
