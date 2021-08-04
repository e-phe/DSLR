#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import os
import re
import sys

def hist(data, gryffindor, hufflepuff, ravenclaw, slytherin):
	for i in range(0, len(data[0])):
		plt.hist(gryffindor[:, i], color='red', bins=25, alpha=0.5)
		plt.hist(hufflepuff[:, i], color='yellow', bins=25, alpha=0.5)
		plt.hist(ravenclaw[:, i], color='blue', bins=25, alpha=0.5)
		plt.hist(slytherin[:, i], color='green', bins=25, alpha=0.5)
		plt.legend(['Grynffindor', 'Hufflepuff', 'Ravenclaw', 'Slytherin'], loc='upper right', frameon=False)
		plt.title(data[0, i])
		plt.xlabel('Grades')
		plt.ylabel('Number of student')
		plt.show()

def ft_count(data, i):
	count = 0
	for j in range(1, len(data[:, i])):
		if data[j, i] != "":
			count += 1
	return count

def ft_mean(data, i):
	sum = 0
	for j in range(1, len(data[:, i])):
		if data[j, i] != "":
			sum += float(data[j, i])
	return sum / ft_count(data, i)

def ft_sqrt(nb):
	diff = 1
	a = nb
	if nb <= 0:
		return 0
	while diff > 0.001:
		b = 0.5 * (a + nb / a)
		diff = a - b
		a = b
	return a

def ft_std(data, i):
	std = 0
	m = ft_mean(data, i)
	for j in range(1, len(data[:, i])):
		if data[j, i] != "":
			std += (float(data[j, i]) - m) * (float(data[j, i]) - m)
	return ft_sqrt(std / (ft_count(data, i) - 1))

def standardization(data, house):
	ret = np.zeros([len(house), len(house[0])], dtype="float")
	for i in range(0, len(data[0])):
		mean = ft_mean(data, i)
		std = ft_std(data, i)
		for j in range(1, len(house[:, i])):
			if house[j, i] != "":
				ret[j, i] = (float(house[j, i]) - mean) / std
	return ret

def delCoLette(data, i):
	for j in range(1, len(data[:, i])):
		if data[j, i] != "" and re.search("^[+-]?([0-9]+[.])?[0-9]+$", data[j, i]) == None:
			return [np.delete(data, i, 1), i]
	return [data, i + 1]

def removeLetter(house):
	house = np.delete(house, 0, 1)
	i = 0
	while i < len(house[0]):
		[house, i] = delCoLette(house, i)
	return house

def parseHouse(data):
	gryffindor = np.zeros([0, len(data[0])])
	hufflepuff = np.zeros([0, len(data[0])])
	ravenclaw = np.zeros([0, len(data[0])])
	slytherin = np.zeros([0, len(data[0])])
	for i in range(0, len(data[:, 0])):
		if data[i, 1] == "Gryffindor":
			gryffindor = np.append(gryffindor, np.array([data[i, :]]), axis=0)
		elif data[i, 1] == "Hufflepuff":
			hufflepuff = np.append(hufflepuff, np.array([data[i, :]]), axis=0)
		elif data[i, 1] == "Ravenclaw":
			ravenclaw = np.append(ravenclaw, np.array([data[i, :]]), axis=0)
		elif data[i, 1] == "Slytherin":
			slytherin = np.append(slytherin, np.array([data[i, :]]), axis=0)
	data = removeLetter(data)
	gryffindor = removeLetter(gryffindor)
	hufflepuff = removeLetter(hufflepuff)
	ravenclaw = removeLetter(ravenclaw)
	slytherin = removeLetter(slytherin)
	gryffindor = standardization(data, gryffindor)
	hufflepuff = standardization(data, hufflepuff)
	ravenclaw = standardization(data, ravenclaw)
	slytherin = standardization(data, slytherin)
	hist(data, gryffindor, hufflepuff, ravenclaw, slytherin)

def checkError():
	try:
		if len(sys.argv) == 2 and os.path.isfile(sys.argv[1]) and os.stat(sys.argv[1]).st_size > 0:
			data = np.loadtxt(sys.argv[1], dtype = str, delimiter = ",")
			if (len(data[:, 0]) >= 2):
				return data
	except:
		pass
	print("Error")
	exit(1)

if __name__ == "__main__":
	data = checkError()
	parseHouse(data)
