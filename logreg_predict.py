#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import argparse
import numpy as np
import pandas as pd
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
    df = np.apply_along_axis(standardization, 0, np.array(df))
    houses = []
    for i in df:
        houses.append(
            max((np.nansum(i * np.array(theta[house])), house) for house in theta)[1]
        )
    return houses


def parse():
    parser = argparse.ArgumentParser(
        description="",
    )
    parser.add_argument("dataset_test.csv", help="testing dataset")
    parser.add_argument("theta.csv", help="weight to make the prediction")
    args = parser.parse_args()
    try:
        df = pd.read_csv(sys.argv[1], index_col="Index")
        theta = pd.read_csv(sys.argv[2])
    except:
        sys.exit("Error")
    if df.empty or theta.empty:
        sys.exit("Error")
    return [df, theta]


if __name__ == "__main__":
    [df, theta] = parse()
    houses = predict(df.iloc[:, 5:], theta)
    houses = pd.DataFrame(houses, columns=["Hogwarts House"])
    houses.index.name = "Index"
    houses.to_csv("houses.csv")
