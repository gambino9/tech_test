import os
import csv
import pandas as pd
import numpy as np
from collections import Counter
import datetime

# Parsing :
# ASKED
# - Missing lines (non-contiguous time-series)      YES
# - 0s in columns (warning instead of error)        YES
# - Incoherent datas                                YES (range)
# OTHERS
# - Check for N/A values (dropping the columns)     YES
# - Warning when float is found in volume column ?  NO

# ANALYSIS :
# - At the end of each file processing, display some metrics about data distribution
# that you think can be helpful to spot anomalies, like statistics for example.


def find_missing_lines(df):
    if any(df.isna()):
        print("unfilled data")
    # Remove missing values
    df = df.dropna()
    return df


def check_date_time_continuity(df):
    """
    Check datetime discontinuity on a daily increasing basis
    :param df:
    :return:
    """
    d = pd.DatetimeIndex(df['Date'])
    print(d)
    i = 0
    discontinuities = 0
    while i < len(d) - 1:
        print(d[i] - d[i + 1])
        if d[i] - d[i + 1] != -1:
            discontinuities += 1
        i += 1


def check_values_range(df):
    """
    Checks if sentiment values are between 0 and 1
    :param df: dataframe
    :return:
    """
    print(all(df['sentiment_positive'].between(0, 1)))
    print(all(df['sentiment_negative'].between(0, 1)))
    print(all(df['emotion_joy'].between(0, 1)))
    print(all(df['emotion_fear'].between(0, 1)))

    # Remove rows containing sentiment values outside 0-1 range
    d1 = df[df['emotion_joy'].between(0, 1)]
    print(d1)


def check_for_zero_values(df):
    """
    Counts numbers of zero values in each column of the dataframe
    :param df:
    :return:
    """
    # print(df)
    # print(df.eq(0).any())
    # print(Counter(df.eq(0).any()))
    # zeros_df = df[df['emotion_fear'] == 0]
    zeros_df = df.isin([0]).sum(axis=0)
    print(sum(zeros_df))


def print_csv_file_analysis(df):
    """
    Prints
    :param df:
    :return:
    """


if __name__ == "__main__":
    dirname = os.path.dirname(__file__)
    csv_file = os.path.join(dirname, '../resources/test_file (copie).csv')
    # csv_file = os.path.join(dirname, '../resources/test_file.csv')
    dataframe = pd.read_csv(csv_file)  # TODO : Read excel files (and JSON ?)
    # print(dataframe)
    # find_missing_lines(dataframe)
    # check_values_range(dataframe)
    check_date_time_continuity(dataframe)
    # check_for_zero_values(dataframe)
