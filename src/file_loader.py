import sys
import pandas as pd


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
