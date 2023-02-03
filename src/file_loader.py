import sys

import pandas as pd
import os


class FileLoader:
    """
    The goal of this class is to load any CSV, Excel or Json file as a pandas Dataframe
    """
    def __init__(self):
        pass

    def load_file(self, path):
        try:
            if path.endswith("csv"):
                dataframe = pd.read_csv(path)
            elif path.endswith("xls") or path.endswith("xlsx"):
                dataframe = pd.read_excel(path)
            elif path.endswith("json"):
                dataframe = pd.read_json(path, encoding='unicode_escape')
            else:
                raise FileNotFoundError
            return dataframe
        except AttributeError as err:
            sys.exit(err)


if __name__ == "__main__":
    dirname = os.path.dirname(__file__)
    # csv_file = os.path.join(dirname, '../resources/test_file (copie).csv')
    # csv_file = os.path.join(dirname, '../resources/Test_file.xlsx')
    csv_file = os.path.join(dirname, '../resources/epl_2022_2023_30_01_2023.json')
    FileLoader = FileLoader()
    df = FileLoader.load_file(csv_file)
    print(df)
