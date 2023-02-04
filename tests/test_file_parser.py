import unittest
import numpy as np
import pandas as pd
from src.file_parser import FileParser


class FileParserTest(unittest.TestCase):
    columns = ["Date", "sentiment_positive", "sentiment_negative", "emotion_joy", "emotion_fear", "volume"]

    def test_find_missing_values(self):
        """
        Checks if NaN values are found in dataset
        """
        data = [["2020-01-01 00:00:00", 1, 2, 3, 4, 5],
                ["2020-01-02 00:00:00", np.nan, 6, 7, np.nan, np.nan],
                ["2020-01-03 00:00:00", 8, 9, 10, np.nan, 10]]
        df = pd.DataFrame(data, columns=self.columns)

        file_parser = FileParser(df)

        self.assertEqual(file_parser.nan_sentiment_values, 3)
        self.assertEqual(file_parser.nan_volume_values, 1)

    def test_time_continuity(self):
        """
        Checks if the day missing from the dataset is detected
        """
        data = [["2020-01-01 00:00:00", 1, 2, 3, 4, 5],
                ["2020-01-02 00:00:00", np.nan, 6, 7, np.nan, np.nan],
                ["2020-01-04 00:00:00", 8, 9, 10, np.nan, 10],
                ["2020-01-05 00:00:00", 8, 9, 10, np.nan, 10]]

        df = pd.DataFrame(data, columns=self.columns)

        file_parser = FileParser(df)

        self.assertEqual(file_parser.date_time_continuity, 1)

    def test_find_zero_values(self):
        """
        Checks if zero values are found
        """
        data = [["2020-01-01 00:00:00", 1, 0, 3, 4, 0],
                ["2020-01-02 00:00:00", 0, 6, 7, 0, np.nan],
                ["2020-01-03 00:00:00", 8, 9, 0, np.nan, 0]]
        df = pd.DataFrame(data, columns=self.columns)

        file_parser = FileParser(df)

        self.assertEqual(file_parser.zeros_sentiment_values, 4)
        self.assertEqual(file_parser.zeros_volume_values, 2)

    def test_find_outliers(self):
        pass

    def test_find_float_values_in_volume_column(self):
        """
        Checks if float values in volume volumn are found
        """
        data = [["2020-01-01 00:00:00", 1, 0, 3, 4, 0.7],
                ["2020-01-02 00:00:00", 0, 6, 7, 0, 0],
                ["2020-01-03 00:00:00", 8, 9, 0, np.nan, 4.2]]
        df = pd.DataFrame(data, columns=self.columns)

        file_parser = FileParser(df)

        self.assertEqual(file_parser.float_volume_values, 2)


if __name__ == '__main__':
    unittest.main()
