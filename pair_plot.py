#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import argparse
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create a pair plot that help answer the following question : which characteristics will you use to train your coming logistic regressions?",
    )
    parser.add_argument("dataset_train.csv", help="dataset to use")
    args = parser.parse_args()
    try:
        df = pd.read_csv(sys.argv[1], index_col="Index")
    except:
        sys.exit("Error")
    df = df[["Hogwarts House"] + list(df.select_dtypes(include="number"))].dropna()
    if df.empty:
        sys.exit("Error")
    sns.pairplot(df, hue="Hogwarts House")
    plt.show()
