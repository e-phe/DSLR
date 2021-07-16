#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import numpy as np
import os
import re
import sys

def printDescribe(describe, printLen):
	printDescribe = ""
	for j in range(0, len(describe[:, 0])):
		for i in range(0, len(describe[0])):
			if i == 0:
				printDescribe += describe[j, i].ljust(int(printLen[i]))
			else:
				if re.search("^[+-]?([0-9]+[.])?[0-9]+$", describe[j, i]) == None:
					printDescribe += describe[j, i].rjust(int(printLen[i]))
				else:
					printDescribe += str("%.6f" % float(describe[j, i])).rjust(int(printLen[i]))
			printDescribe += "  "
		printDescribe += '\n'
	print(printDescribe[:-1])

def maxLen(describe, i):
	max = float('-inf')
	for j in range(0, len(describe[:, i])):
		if re.search("^[+-]?([0-9]+[.])?[0-9]+$", describe[j, i]) == None and len(describe[j, i]) > max:
			max = len(describe[j, i])
		elif re.search("^[+-]?([0-9]+[.])?[0-9]+$", describe[j, i]) != None and len("%.6f" % float(describe[j, i])) > max:
			max = len("%.6f" % float(describe[j, i]))
	return max

def ft_count(data, i):
	if i == 0:
		return "Count"
	count = 0
	for j in range(1, len(data[:, i - 1])):
		if data[j, i - 1] != "":
			count += 1
	return count

def ft_mean(data, i):
	if i == 0:
		return "Mean"
	if ft_count(data, i) == 0:
		return "NaN"
	sum = 0
	for j in range(1, len(data[:, i - 1])):
		if data[j, i - 1] != "":
			sum += float(data[j, i - 1])
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
	if i == 0:
		return "Std"
	if ft_count(data, i) == 0:
		return "NaN"
	std = 0
	m = ft_mean(data, i)
	for j in range(1, len(data[:, i - 1])):
		if data[j, i - 1] != "":
			std += (float(data[j, i - 1]) - m) * (float(data[j, i - 1]) - m)
	return ft_sqrt(std / (ft_count(data, i) - 1))

def ft_min(data, i):
	if i == 0:
		return"Min"
	if ft_count(data, i) == 0:
		return "NaN"
	min = float('inf')
	for j in range(1, len(data[:, i - 1])):
		if data[j, i - 1] != "" and float(data[j, i - 1]) < min:
			min = float(data[j, i - 1])
	return min

def ft_firstQuartile(data, i):
	if i == 0:
		return "25%"
	if ft_count(data, i) == 0:
		return "NaN"
	tab = []
	for j in range(1, len(data[:, i - 1])):
		if data[j, i - 1] != "":
			tab.append(float(data[j, i - 1]))
	tab.sort()
	quarter = (len(tab) - 1) / 4
	down = np.floor(quarter)
	up = np.ceil(quarter)
	if down == up:
		return tab[int(quarter)]
	return tab[int(down)] * (up - quarter) + tab[int(up)] * (quarter - down)

def ft_median(data, i):
	if i == 0:
		return "50%"
	if ft_count(data, i) == 0:
		return "NaN"
	tab = []
	for j in range(1, len(data[:, i - 1])):
		if data[j, i - 1] != "":
			tab.append(float(data[j, i - 1]))
	tab.sort()
	half = int(len(tab) / 2)
	if len(tab) % 2 != 0:
		return tab[half]
	return (tab[half - 1] + tab[half]) / 2

def ft_thirdQuartile(data, i):
	if i == 0:
		return "75%"
	if ft_count(data, i) == 0:
		return "NaN"
	tab = []
	for j in range(1, len(data[:, i - 1])):
		if data[j, i - 1] != "":
			tab.append(float(data[j, i - 1]))
	tab.sort()
	quarter = ((len(tab) - 1) / 4) * 3
	down = np.floor(quarter)
	up = np.ceil(quarter)
	if down == up:
		return tab[int(quarter)]
	return tab[int(down)] * (up - quarter) + tab[int(up)] * (quarter - down)

def ft_max(data, i):
	if i == 0:
		return "Max"
	if ft_count(data, i) == 0:
		return "NaN"
	max = float('-inf')
	for j in range(1, len(data[:, i - 1])):
		if data[j, i - 1] != "" and float(data[j, i - 1]) > max:
			max = float(data[j, i - 1])
	return max

def delCoLette(data, i):
	for j in range(1, len(data[:, i - 1])):
		if data[j, i] != "" and re.search("^[+-]?([0-9]+[.])?[0-9]+$", data[j, i]) == None:
			return [np.delete(data, i, 1), i]
	return [data, i + 1]

def checkError():
	try:
		if (os.path.isfile(sys.argv[1]) and os.stat(sys.argv[1]).st_size > 0):
			data = np.loadtxt(sys.argv[1], dtype = str, delimiter = ",")
			if (len(data[:, 0]) >= 2):
				return data
	except:
		pass
	print("Error")
	exit(1)

if __name__ == "__main__":
	if len(sys.argv) < 2:
		exit(1)
	data = checkError()
	i = 0
	while i < len(data[0]):
		[data, i] = delCoLette(data, i)
	options = {
		1: ft_count,
		2: ft_mean,
		3: ft_std,
		4: ft_min,
		5: ft_firstQuartile,
		6: ft_median,
		7: ft_thirdQuartile,
		8: ft_max,
	}
	describe = np.zeros([len(options) + 1, len(data[0]) + 1], dtype="<U1000")
	describe[0, 1:] = data[0]
	printLen = np.zeros(len(describe[0]), dtype="<U1000")
	for i in range(0, len(describe[0])):
		for j in range(1, len(describe[:, 0])):
				describe[j, i] = options[j](data, i)
		printLen[i] = maxLen(describe, i)
	printDescribe(describe, printLen)
