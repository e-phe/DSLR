#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import argparse
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys


def scatterPlot(df, features):
    plt.xlabel(df[0, features[0]])
    plt.ylabel(df[0, features[1]])
    plt.scatter(df[1:, features[0]].astype(float), df[1:, features[1]].astype(float))
    plt.show()


def similarFeatures(df):
    longest = 0
    features = []
    for i in range(0, len(df[0])):
        for j in range(i + 1, len(df[0])):
            similarities = len(set(df[1:, i]) & set(df[1:, j]))
            if longest < similarities:
                longest = similarities
                features = [i, j]
    return features


def prepData(df):
    for i in range(0, len(df[0])):
        for j in range(1, len(df)):
            df[j, i] = str(abs(float(df[j, i]))).replace(".", "")
    return df


def parse():
    parser = argparse.ArgumentParser(
        description="Create a scatter plot that help answer the following question : which two features are similar?",
    )
    parser.add_argument("dataset_train.csv", help="dataset to use")
    args = parser.parse_args()
    try:
        df = pd.read_csv(sys.argv[1], index_col="Index")
    except:
        sys.exit("Error")
    df = df.select_dtypes(exclude=[object])
    if df.empty:
        sys.exit("Error")
    return df


if __name__ == "__main__":
    df = parse()
    col = np.array(df.columns)
    df = np.array(df, dtype="<U1000")
    df = np.insert(df, 0, col, axis=0)
    features = similarFeatures(prepData(df.copy()))
    scatterPlot(df, features)
