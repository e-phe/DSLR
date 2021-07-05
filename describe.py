#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import numpy as np
import os
import pandas as pd
import re

def count(data, i):
	if i == 0:
		return "Count"
	count = 0
	for j in range(1, len(data[:, 0])):
		if data[j, i - 1] != "":
			count += 1
	return count

def mean(data, i):
	if i == 0:
		return "Mean"
	if count(data, i) == 0:
		return "NaN"
	sum = 0
	for j in range(1, len(data[:, 0])):
		if data[j, i - 1] != "":
			sum += float(data[j, i - 1])
	return sum / count(data, i)

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

def std(data, i):
	if i == 0:
		return "Std"
	if count(data, i) == 0:
		return "NaN"
	std = 0
	m = mean(data, i)
	for j in range(1, len(data[:, 0])):
		if data[j, i - 1] != "":
			std += (float(data[j, i - 1]) - m) * (float(data[j, i - 1]) - m)
	return sqrt(std / (count(data, i) - 1))

def min(data, i):
	if i == 0:
		return"Min"
	min = 0
	for j in range(1, len(data[:, 0])):
		if data[j, i - 1] != "" and float(data[j, i - 1]) < min:
			min = float(data[j, i - 1])
	return min

def median(data, i):
	if i == 0:
		return "50%"
	if count(data, i) == 0:
		return "NaN"
	tab = []
	for j in range(1, len(data[:, 0])):
		if data[j, i - 1] != "":
			tab.append(float(data[j, i - 1]))
	tab.sort()
	half = int(len(tab) / 2)
	if not len(tab) % 2:
		return (tab[half - 1] + tab[half]) / 2
	return tab[half]

def max(data, i):
	if i == 0:
		return "Max"
	max = 0
	for j in range(1, len(data[:, 0])):
		if data[j, i - 1] != "" and float(data[j, i - 1]) > max:
			max = float(data[j, i - 1])
	return max

def delColumn(data, i):
	for j in range(1, len(data[:, 0])):
		if data[j, i] != "" and (re.search("[+-]?([0-9]+[.])?[0-9]+", data[j, i]) == None or
		len(re.findall("[+-]?([0-9]+[.])?[0-9]+", data[j, i])) != 1):
			return [np.delete(data, i, 1), i]
	return [data, i + 1]

def checkError():
	try:
		if (os.path.isfile("datasets/dataset_test.csv") and os.stat("datasets/dataset_test.csv").st_size > 0):
			data = np.loadtxt("datasets/dataset_test.csv", dtype = str, delimiter = ",")
			if (len(data[:, 0]) >= 2):
				return data
	except:
		pass
	print("Error")
	exit(1)

if __name__ == "__main__":
	# df = pd.read_csv("datasets/dataset_test.csv")
	# print(df.describe())
	data = checkError()
	i = 0
	while i < len(data[0]):
		[data, i] = delColumn(data, i)
	options = {
		1: count,
		2: mean,
		3: std,
		4: min,
		# 5: twentyFive,
		5: median,
		# 7: seventyFive,
		6: max,
	}
	describe = np.zeros([len(options) + 1, len(data[0]) + 1], dtype="<U1000")
	describe[0, 1:] = data[0]
	i = 0
	while i < len(describe[0]):
		for j in range(1, len(describe[:, 0])):
			describe[j, i] = options[j](data, i)
		i += 1
