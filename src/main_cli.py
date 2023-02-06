from file_loader import FileLoader
from file_parser import FileParser
import click


@click.command()
@click.argument("file", type=click.Path(exists=True))
def main(file):
    """
    The script takes a file path to analyze a dataset and print results

    FILE is the argument path
    """
    file_loader = FileLoader()
    dataframe = file_loader.load_file(file)

    file_parser = FileParser(dataframe)
    analysis = file_parser.return_file_analysis()
    print(analysis)


if __name__ == "__main__":
    main()
