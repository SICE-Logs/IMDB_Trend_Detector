import pathlib 
PROJECT_ROOT = pathlib.Path(__file__).parent.parent.absolute()

RAW_DATA_PATH = PROJECT_ROOT/"data"/"IMDB_Raw_Movies.csv"
PREPROCESSED_DATA_PATH = PROJECT_ROOT/"data"/"IMDB_Cleaned_Movies.csv"
DATABASE_PATH = PROJECT_ROOT/"movies.db"

DATA_DIR = PROJECT_ROOT/"data"

NOTEBOOKS_DIR = PROJECT_ROOT/"notebooks"

SRC_DIR = PROJECT_ROOT/"src"
