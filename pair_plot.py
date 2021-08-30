#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns
import sys

if __name__ == "__main__":
	try:
		if os.stat("datasets/dataset_train.csv").st_size > 0:
			data = pd.read_csv("datasets/dataset_train.csv")
		else:
			sys.exit("Error")
	except:
		sys.exit("Error")
	data.drop('Index', axis=1, inplace=True)
	data = data[["Hogwarts House"] + list(data.select_dtypes(include="number"))].dropna()
	sns.pairplot(data, hue="Hogwarts House")
	plt.show()
