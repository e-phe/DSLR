#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import sys

def sigmoid(x):
	return 1 / (1 + np.exp(-x))

def gradientDescent(X, y, theta):
	alpha = 0.1
	m = len(y)
	for i in range(0, 20000):
		z = np.dot(X, theta)
		h = sigmoid(z)
		gradient = np.dot(np.transpose(X), (h - y))
		theta -= (alpha / m) * gradient
	return theta

def sqrt(nb):
	diff = 1
	a = nb
	if nb <= 0:
		return 0
	while diff > 0.001:
		b = 0.5 * (a + nb / a)
		diff = a - b
		a = b
	return a

def standardization(data):
	mean = sum(data) / len(data)
	std = 0
	for number in data:
		std += (number - mean) * (number - mean)
	std = sqrt(std / len(data))
	for i in range(len(data)):
		data[i] = (data[i] - mean) / std
	return data

def fit(X, y):
	np.apply_along_axis(standardization, 0, X)
	theta = []
	for i in np.unique(y):
		tmpTheta = gradientDescent(X, np.where(y == i, 1, 0), np.zeros(X.shape[1]))
		theta.append((i, tmpTheta))
	return theta

if __name__ == "__main__":
	try:
		df = pd.read_csv(sys.argv[1], index_col = "Index")
	except:
		sys.exit("Error")
	if (not len(df)):
		sys.exit("Error")
	df = df.dropna()
	theta = fit(np.array(df.iloc[:,5:]), np.array(df.loc[:,"Hogwarts House"]))
	pd.DataFrame(theta,).to_csv("theta.csv", index=False)
