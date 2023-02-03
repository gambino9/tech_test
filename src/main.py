import os
import pandas as pd
from file_loader import FileLoader
from file_parser import FileParser


if __name__ == "__main__":
    dirname = os.path.dirname(__file__)
    data_file = os.path.join(dirname, '../resources/test_file (copie).csv')
    # csv_file = os.path.join(dirname, '../resources/test_file.csv')
    file_loader = FileLoader()
    dataframe = file_loader.load_file(data_file)

    file_parser = FileParser()

    # file_parser.find_missing_values(dataframe)
    file_parser.check_float_values_in_volume_column(dataframe)
    # check_values_range(dataframe)
    # print(check_date_time_continuity(dataframe))
    # check_for_zero_values(dataframe)
    # check_outliers(dataframe)
