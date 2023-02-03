import os
import csv
import pandas as pd
import numpy as np


# Parsing :
# ASKED
# - Missing lines (non-contiguous time-series)      YES
# - 0s in columns (warning instead of error)        YES
# - Incoherent datas                                YES
# OTHERS
# - Check for N/A values (dropping the columns)     YES
# - Warning when float is found in volume column ?  NO

# ANALYSIS :
# - At the end of each file processing, display some metrics about data distribution
# that you think can be helpful to spot anomalies, like statistics for example.


class FileParser:
    def __init__(self):
        pass

    def find_missing_values(self, df):
        """
        Finds in the dataset all NaN (missing values) in the sentiments columns and the volume's column
        :param df: Dataset
        :return:
        """
        if any(df.isna()):
            nan_total = df.isna().sum()  # A dataset containing nb of NaN for each column
            sentiment_nan = sum(nan_total[['sentiment_positive', 'sentiment_negative', 'emotion_joy', 'emotion_fear']])
            volume_nan = nan_total['volume']
            print(f"There are {sentiment_nan} NaN values in sentiment datas, and {volume_nan} in volume")
        # Remove missing values ?
        df = df.dropna()
        return df

    def check_date_time_continuity(self, df):  # Must tell how many missing lines are there
        """
        Iterates through dataset to check datetime discontinuity on a daily increasing basis

        :param df: Time-series dataset
        :return: Number of missing days in dataset
        """
        d = pd.DatetimeIndex(df['Date'])
        i = 0
        discontinuities = 0
        while i < len(d) - 1:
            # Subtract 2 contiguous rows
            # Subtract that result by a one day TimeDelta to spot more easily discontinuities
            # Divide dy day TimeDelta to retrieve the float value
            # Increment each discontinuity to the variable
            discontinuities += (d[i] - d[i + 1] - pd.Timedelta(-1, "d")) / pd.Timedelta(days=1)
            i += 1
        return abs(int(discontinuities))

    def check_outliers(self, df):
        """
        Checks for outliers values, values too far from the average by applying the inter quartile range method
        :param df: Dataset
        :return:
        """
        # inter quartile range method
        q25, q75 = df['sentiment_negative'].quantile(0.25), df['sentiment_negative'].quantile(0.75)
        iqr = q75 - q25
        cut_off = iqr * 1.5
        lower, upper = q25 - cut_off, q75 + cut_off
        outliers = [x for x in df['sentiment_negative'] if x < lower or x > upper]
        print(outliers)

        # data_mean, data_std = np.mean(df['sentiment_negative']), np.std(df['sentiment_negative'])
        # cut_off = data_std * 3  # 1.3
        # lower, upper = data_mean - cut_off, data_mean + cut_off
        #
        # outliers = [x for x in df['sentiment_negative'] if x < lower or x > upper]
        # print(outliers)

    def check_for_zero_values(self, df):
        """
        Counts numbers of zero values in each column of the dataframe
        :param df:
        :return:
        """
        zeros_df = df.isin([0]).sum(axis=0)
        if sum(zeros_df):
            sentiment_zeros = sum(zeros_df[['sentiment_positive', 'sentiment_negative', 'emotion_joy', 'emotion_fear']])
            volume_zeros = zeros_df['volume']
            print(sentiment_zeros)
            print(volume_zeros)
        print(sum(zeros_df))

    def check_float_values_in_volume_column(self, df):
        """
        Counts number of zero values in the dataset
        :param df:
        :return:
        """
        volume_series = df['volume']
        if float_values := sum(not float(x).is_integer() for x in volume_series):
            print(f"Warning : There are {float_values} in the volume column")

    def print_csv_file_analysis(self, df):
        """
        Prints
        :param df:
        :return:
        """


