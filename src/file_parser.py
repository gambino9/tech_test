import pandas as pd


# Parsing :
# ASKED
# - Missing lines (non-contiguous time-series)      YES
# - 0s in columns (warning instead of error)        YES
# - Incoherent datas                                YES
# OTHERS
# - Check for N/A values (dropping the columns)     YES
# - Warning when float is found in volume column ?  YES

# ANALYSIS :
# - At the end of each file processing, display some metrics about data distribution
# that you think can be helpful to spot anomalies, like statistics for example.


class FileParser:
    def __init__(self, df):
        self.df = df

        self.nan_sentiment_values, self.nan_volume_values = self.find_missing_values()  # validity : no
        self.date_time_continuity = self.check_date_time_continuity()  # validity : no
        self.zeros_sentiment_values, self.zeros_volume_values = self.check_for_zero_values()  # validity : yes (warning)
        self.float_volume_values = self.check_float_values_in_volume_column()  # validity : no

    def find_missing_values(self):
        """
        Finds in the dataset all NaN (missing values) in the sentiments columns and
        the volume's column
        :return: Tuple of number of NaN in the sentiments columns and number of Nan in volume column
                 Tuple of None objects if no NaN values were found
        """
        if any(self.df.isna()):
            nan_total = self.df.isna().sum()  # A dataset containing nb of NaN for each column
            nan_sentiment_values = sum(nan_total[['sentiment_positive', 'sentiment_negative', 'emotion_joy', 'emotion_fear']])
            nan_volume_values = nan_total['volume']
            return nan_sentiment_values, nan_volume_values
        return None, None

    def check_date_time_continuity(self):  # Must tell how many missing lines are there
        """
        Iterates through DatetimeIndex obj from Date column of dataset to check
        datetime discontinuity on a daily increasing basis

        :return: Absolute value of missing days in dataset
        """
        d = pd.DatetimeIndex(self.df['Date'])
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

    def check_for_zero_values(self):
        """
        Counts numbers of zero values in each column of the dataframe
        :return: Tuple containing number of zeros in sentiment columns and in volume column
                 Tuple of None objects if no zero values found
        """
        zeros_df = self.df.isin([0]).sum(axis=0)
        if sum(zeros_df):
            zeros_sentiment_values = sum(zeros_df[['sentiment_positive', 'sentiment_negative', 'emotion_joy', 'emotion_fear']])
            zeros_volume_values = zeros_df['volume']
            return zeros_sentiment_values, zeros_volume_values
        return None, None

    def check_outliers(self, column_name):
        """
        For a given column, checks for outliers values (values too far
        from the average) by applying the interquartile range method
        :return: List containing outliers values
        """
        # inter quartile range method
        q25, q75 = self.df[column_name].quantile(0.25), self.df[column_name].quantile(0.75)
        iqr = q75 - q25
        cut_off = iqr * 0.5
        lower, upper = q25 - cut_off, q75 + cut_off
        outliers = [x for x in self.df[column_name] if x < lower or x > upper]
        return outliers

        # data_mean, data_std = np.mean(df['sentiment_negative']), np.std(df['sentiment_negative'])
        # cut_off = data_std * 3  # 1.3
        # lower, upper = data_mean - cut_off, data_mean + cut_off
        #
        # outliers = [x for x in df['sentiment_negative'] if x < lower or x > upper]
        # print(outliers)

    def check_float_values_in_volume_column(self):
        """
        Counts number of zero values in the dataset
        :return: Number of float values in volume column, else None
        """
        volume_series = self.df['volume']
        if float_values := sum(not float(x).is_integer() for x in volume_series):
            return float_values
        return None

    def is_dataset_valid(self):
        pass

    def print_csv_file_analysis(self):
        pass


