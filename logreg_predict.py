#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import re
import sys


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


def predict(df, theta):
    df = df.dropna()
    df = np.apply_along_axis(standardization, 0, np.array(df))
    houses = []
    for i in df:
        houses.append(
            max((np.dot(i, np.array(theta[house])), house) for house in theta)[1]
        )
    return houses


if __name__ == "__main__":
    try:
        df = pd.read_csv(sys.argv[1], index_col="Index")
        theta = pd.read_csv(sys.argv[2])
    except:
        sys.exit("Error")
    if not len(df) or not len(theta):
        sys.exit("Error")
    houses = predict(df.iloc[:, 5:], theta)
    houses = pd.DataFrame(houses, columns=["Hogwarts House"])
    houses.index.name = "Index"
    houses.to_csv("houses.csv")
