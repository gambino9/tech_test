import pandas as pd


def calculate_percentage(part, total):
    if part is None:
        return 0
    average = 100 * float(part) / float(total)
    return average


class FileParser:
    def __init__(self, df):
        self.df = df

        self.sentiment_columns = [
            "sentiment_positive",
            "sentiment_negative",
            "emotion_joy",
            "emotion_fear",
        ]

        self.date_time_continuity = self.check_date_time_continuity()
        (
            self.zeros_sentiment_values,
            self.zeros_volume_values,
        ) = self.check_for_zero_values()
        self.nb_outliers = sum(
            len(self.check_outliers(x)) for x in self.sentiment_columns
        )
        self.nan_sentiment_values, self.nan_volume_values = self.find_missing_values()
        self.float_volume_values = self.check_float_values_in_volume_column()

        self.warning = False
        self.invalid = False

        self.analysis = ""

        self.check_dataset_validity()

    def find_missing_values(self):
        """
        Finds in the dataset all NaN (missing values) in the sentiments columns and
        the volume's column
        :return: Tuple of number of NaN in the sentiments columns and number of Nan in volume column
                 Tuple of None objects if no NaN values were found
        """
        if any(self.df.isna()):
            nan_total = (
                self.df.isna().sum()
            )  # A dataset containing nb of NaN for each column
            nan_sentiment_values = sum(nan_total[self.sentiment_columns])
            nan_volume_values = nan_total["volume"]
            return nan_sentiment_values, nan_volume_values
        return None, None

    def check_date_time_continuity(self):
        """
        Iterates through dataset to check
        datetime discontinuity on a daily increasing basis

        :return: Absolute value of missing days in dataset
        """
        d = pd.DatetimeIndex(self.df["Date"])
        i = 0
        discontinuities = 0
        while i < len(d) - 1:
            # Subtract 2 contiguous rows
            # Subtract that result by a one day TimeDelta to spot more easily discontinuities
            # Divide dy day TimeDelta to retrieve the float value
            # Increment each discontinuity to the variable
            discontinuities += (d[i] - d[i + 1] - pd.Timedelta(-1, "d")) / pd.Timedelta(
                days=1
            )
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
            zeros_sentiment_values = sum(zeros_df[self.sentiment_columns])
            zeros_volume_values = zeros_df["volume"]
            return zeros_sentiment_values, zeros_volume_values
        return None, None

    def check_outliers(self, column_name, k_factor=0.5):
        """
        For a given column, checks for outliers values (values too far
        from the average) by applying the interquartile range method
        :param: column_name : The column where to look for outliers
                k_factor : The factor by which we multiply the interquartile range
                to calculate the threshold. Default is set to 0.5 and can be adapted
        :return: List containing outliers values
        """
        # inter quartile range method
        q25, q75 = self.df[column_name].quantile(0.25), self.df[column_name].quantile(
            0.75
        )
        iqr = q75 - q25
        cut_off = iqr * k_factor
        lower, upper = q25 - cut_off, q75 + cut_off
        outliers = [x for x in self.df[column_name] if x < lower or x > upper]
        return outliers

    def check_float_values_in_volume_column(self):
        """
        Counts number of zero values in the dataset
        :return: Number of float values in volume column, else None
        """
        volume_series = self.df["volume"]
        if float_values := sum(not float(x).is_integer() for x in volume_series):
            return float_values
        return None

    def check_dataset_validity(self):
        """
        Fills bool values if the dataset is invalid or raises any warning
        """
        if any([self.zeros_volume_values, self.zeros_sentiment_values]):
            self.warning = True
        if any(
            [
                self.date_time_continuity,
                self.nb_outliers,
                self.nan_volume_values,
                self.nan_sentiment_values,
                self.float_volume_values,
            ]
        ):
            self.invalid = True

    def return_file_analysis(self):
        """
        File analysis if file has a warning, is invalid or if it is valid
        :return : A concatenated string containing the file analysis
        """
        rows = self.df.shape[0]

        if self.warning:
            self.analysis += f"WARNING : The dataset contains zeros values\n"
            zero_total = self.zeros_sentiment_values + self.zeros_volume_values
            zero_stat = calculate_percentage(zero_total, rows)
            self.analysis += (
                f"Percentage of zeros values : {zero_stat:.2f}% ({self.zeros_volume_values} in volume "
                f"column and {self.zeros_sentiment_values} on sentiments columns)\n"
            )

        if self.invalid:
            self.analysis += f"ERROR : The dataset is invalid\n"

            self.analysis += "\nPlease check the file analysis :\n"

            time_stat = calculate_percentage(self.date_time_continuity, rows)
            self.analysis += f"Percentage of missing days : {time_stat:.2f}% ({self.date_time_continuity} days on {rows} rows)\n"

            outliers_stat = calculate_percentage(self.nb_outliers, rows)
            self.analysis += f"Percentage of outliers values : {outliers_stat:.2f}% (on a DataFrame of shape {self.df.shape})\n"

            nan_total = self.nan_sentiment_values + self.nan_volume_values
            nan_stat = calculate_percentage(nan_total, rows)
            self.analysis += (
                f"Percentage of NaN values : {nan_stat:.2f}% ({self.nan_volume_values} in volume column "
                f"and {self.nan_sentiment_values} in sentiments columns)\n"
            )

            float_stat = calculate_percentage(self.float_volume_values, rows)
            self.analysis += f"Percentage of float values in volume column : {float_stat:.2f}% ({self.float_volume_values} on 86 rows)\n"
        else:
            self.analysis += "The dataset is valid\n"
        return self.analysis
