from file_loader import FileLoader
from file_parser import FileParser
import click


@click.command()
@click.argument('file', type=click.Path(exists=True))
def main(file):
    """
    The script takes a file path to analyze a dataset and print results

    FILE is the argument path
    """
    file_loader = FileLoader()
    dataframe = file_loader.load_file(file)

    file_parser = FileParser(dataframe)
    file_parser.check_dataset_validity()


if __name__ == "__main__":
    main()
