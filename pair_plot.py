#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sys

if __name__ == "__main__":
	try:
		data = pd.read_csv("datasets/dataset_train.csv")
	except:
		sys.exit("Error")
	data.drop('Index', axis=1, inplace=True)
	data = data[["Hogwarts House"] + list(data.select_dtypes(include="number"))].dropna()
	sns.pairplot(data, hue="Hogwarts House")
	plt.show()
