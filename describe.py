#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import argparse
import numpy as np
import pandas as pd
import re
import sys


def printDescribe(describe, printLen):
    printDescribe = ""
    for j in range(len(describe)):
        for i in range(len(describe[0])):
            if i == 0:
                printDescribe += describe[j, i].ljust(int(printLen[i]))
            else:
                if re.search("^[+-]?([0-9]+[.])?[0-9]+$", describe[j, i]) == None:
                    printDescribe += describe[j, i].rjust(int(printLen[i]))
                else:
                    printDescribe += str("%.6f" % float(describe[j, i])).rjust(
                        int(printLen[i])
                    )
            printDescribe += "  "
        printDescribe += "\n"
    print(printDescribe[:-1])


def maxLen(describe, i):
    max = float("-inf")
    for j in range(len(describe)):
        if (
            re.search("^[+-]?([0-9]+[.])?[0-9]+$", describe[j, i]) == None
            and len(describe[j, i]) > max
        ):
            max = len(describe[j, i])
        elif (
            re.search("^[+-]?([0-9]+[.])?[0-9]+$", describe[j, i]) != None
            and len("%.6f" % float(describe[j, i])) > max
        ):
            max = len("%.6f" % float(describe[j, i]))
    return max


def ft_count(df, i):
    if i == 0:
        return "Count"
    count = 0
    for j in range(len(df)):
        if not np.isnan(df[j, i - 1]):
            count += 1
    return count


def ft_mean(df, i):
    if i == 0:
        return "Mean"
    if ft_count(df, i) == 0:
        return "NaN"
    sum = 0
    for j in range(len(df)):
        if not np.isnan(df[j, i - 1]):
            sum += df[j, i - 1]
    return sum / ft_count(df, i)


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


def ft_std(df, i):
    if i == 0:
        return "Std"
    if ft_count(df, i) == 0:
        return "NaN"
    std = 0
    m = ft_mean(df, i)
    for j in range(len(df)):
        if not np.isnan(df[j, i - 1]):
            std += (df[j, i - 1] - m) * (df[j, i - 1] - m)
    return ft_sqrt(std / (ft_count(df, i) - 1))


def ft_min(df, i):
    if i == 0:
        return "Min"
    if ft_count(df, i) == 0:
        return "NaN"
    min = float("inf")
    for j in range(len(df)):
        if not np.isnan(df[j, i - 1]) and df[j, i - 1] < min:
            min = df[j, i - 1]
    return min


def ft_firstQuartile(df, i):
    if i == 0:
        return "25%"
    if ft_count(df, i) == 0:
        return "NaN"
    tab = []
    for j in range(len(df)):
        if not np.isnan(df[j, i - 1]):
            tab.append(df[j, i - 1])
    tab.sort()
    quarter = (len(tab) - 1) / 4
    down = np.floor(quarter)
    up = np.ceil(quarter)
    if down == up:
        return tab[int(quarter)]
    return tab[int(down)] * (up - quarter) + tab[int(up)] * (quarter - down)


def ft_median(df, i):
    if i == 0:
        return "50%"
    if ft_count(df, i) == 0:
        return "NaN"
    tab = []
    for j in range(len(df)):
        if not np.isnan(df[j, i - 1]):
            tab.append(df[j, i - 1])
    tab.sort()
    half = int(len(tab) / 2)
    if len(tab) % 2 != 0:
        return tab[half]
    return (tab[half - 1] + tab[half]) / 2


def ft_thirdQuartile(df, i):
    if i == 0:
        return "75%"
    if ft_count(df, i) == 0:
        return "NaN"
    tab = []
    for j in range(len(df)):
        if not np.isnan(df[j, i - 1]):
            tab.append(df[j, i - 1])
    tab.sort()
    quarter = ((len(tab) - 1) / 4) * 3
    down = np.floor(quarter)
    up = np.ceil(quarter)
    if down == up:
        return tab[int(quarter)]
    return tab[int(down)] * (up - quarter) + tab[int(up)] * (quarter - down)


def ft_max(df, i):
    if i == 0:
        return "Max"
    if ft_count(df, i) == 0:
        return "NaN"
    max = float("-inf")
    for j in range(len(df)):
        if not np.isnan(df[j, i - 1]) and df[j, i - 1] > max:
            max = df[j, i - 1]
    return max


def parse():
    parse = argparse.ArgumentParser(
        description="Descriptive statistics include those that summarize the central tendency, dispersion and shape of a dataset’s distribution, excluding NaN values.",
    )
    parse.add_argument(
        "-d",
        "--describe",
        action="store_true",
        help="display also describe from pandas",
    )
    parse.add_argument("dataset.csv", help="data to analyse")
    args = parse.parse_args()
    try:
        df = pd.read_csv(sys.argv[1])
    except:
        sys.exit("Error")
    df = df.select_dtypes(exclude=[object])
    if df.empty:
        sys.exit("Error")
    if args.describe == True:
        print("Pandas describe\n", df.describe(), "\nMy describe")
    return df


if __name__ == "__main__":
    df = parse()
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
    describe = np.zeros([len(options) + 1, len(np.array(df)[0]) + 1], dtype="<U1000")
    describe[0, 1:] = np.array(df.columns, dtype="<U1000")
    printLen = np.zeros(len(describe[0]), dtype="<U1000")
    df = np.array(df)
    for i in range(len(describe[0])):
        for j in range(1, len(describe)):
            describe[j, i] = options[j](df, i)
        printLen[i] = maxLen(describe, i)
    printDescribe(describe, printLen)
