from src.file_loader import FileLoader
import unittest
import os
import pandas as pd


class FileLoaderTest(unittest.TestCase):

    def test_load_csv_file(self):
        """
        Checks that FileLoader class successfully loads CSV file into a pandas Dataframe
        """
        dirname = os.path.dirname(__file__)
        csv_file = os.path.join(dirname, '../resources/test_file (copie).csv')
        file_loader = FileLoader()
        df = file_loader.load_file(csv_file)

        self.assertIsNot(df, None)
        self.assertIsInstance(df, pd.DataFrame)

    def test_load_excel_file(self):
        """
        Checks that FileLoader class successfully loads Excel file into a pandas Dataframe
        """
        dirname = os.path.dirname(__file__)
        excel_file = os.path.join(dirname, '../resources/Test_file.xlsx')
        file_loader = FileLoader()
        df = file_loader.load_file(excel_file)

        self.assertIsNot(df, None)
        self.assertIsInstance(df, pd.DataFrame)

    def test_load_json_file(self):
        """
        Checks that FileLoader class successfully loads Excel file into a pandas Dataframe
        """
        dirname = os.path.dirname(__file__)
        json_file = os.path.join(dirname, '../resources/epl_2022_2023_30_01_2023.json')
        file_loader = FileLoader()
        df = file_loader.load_file(json_file)

        self.assertIsNot(df, None)
        self.assertIsInstance(df, pd.DataFrame)

    def test_non_existing_file_raises_file_not_found_error(self):
        """
        Checks if non-existing file passed to FileLoader raises a FileNotFoundError
        """
        fake_file = "fake_file"
        file_loader = FileLoader()

        with self.assertRaises(FileNotFoundError):
            df = file_loader.load_file(fake_file)

    def test_wrong_obj_raises_system_exit(self):
        """
        Checks if wrong object passed to FileLoader raises a SystemExit
        """
        fake_file = None
        file_loader = FileLoader()

        with self.assertRaises(SystemExit):
            df = file_loader.load_file(fake_file)


if __name__ == "__main__":
    unittest.main()
