#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import argparse
import numpy as np
import pandas as pd
import sys


def costFunction(h, y):
    m = len(y)
    cost = (
        np.sum(
            np.dot(np.transpose(-y), np.log(h))
            - np.dot(np.transpose(1 - y), np.log(1 - h))
        )
        / m
    )
    print("The precision is " + str(cost))


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def gradientDescent(X, y, theta, args):
    alpha = 0.1
    m = len(y)
    for i in range(0, 20000):
        z = np.dot(X, theta)
        h = sigmoid(z)
        gradient = np.dot(np.transpose(X), (h - y))
        theta -= (alpha / m) * gradient
    if args.precision == True:
        costFunction(h, y)
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


def standardization(X):
    mean = sum(X) / len(X)
    std = 0
    for number in X:
        std += (number - mean) * (number - mean)
    std = sqrt(std / len(X))
    for i in range(len(X)):
        X[i] = (X[i] - mean) / std
    return X


def fit(X, y, args):
    np.apply_along_axis(standardization, 0, X)
    theta = {}
    for i in np.unique(y):
        if args.precision == True:
            print(i)
        tmpTheta = gradientDescent(
            X, np.where(y == i, 1, 0), np.zeros(X.shape[1]), args
        )
        theta[i] = tmpTheta
    return theta


def parse():
    parser = argparse.ArgumentParser(
        description="Multi-classifier using logistic regression in one-vs-all. Training the model with gradient descent.",
    )
    parser.add_argument("dataset_train.csv", help="training dataset")
    parser.add_argument(
        "-p",
        "--precision",
        action="store_true",
        help="displays the precision of the algorithm.",
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse()
    try:
        df = pd.read_csv(sys.argv[1], index_col="Index")
    except:
        sys.exit("Error")
    df = df.dropna(subset=["Astronomy"])
    df = df.dropna(subset=["Herbology"])
    df = df.dropna(subset=["Defense Against the Dark Arts"])
    df = df.dropna(subset=["Ancient Runes"])
    if df.empty:
        sys.exit("Error")
    theta = fit(
        np.array(df.values[:, [6, 7, 8, 11]], dtype=float),
        np.array(df.loc[:, "Hogwarts House"]),
        args,
    )
    pd.DataFrame(theta).to_csv("weights.csv", index=False)
