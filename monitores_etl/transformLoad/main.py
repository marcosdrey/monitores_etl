import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

from monitores_etl.transformLoad.data_manager import DataManager

load_dotenv()

DATA_PATH = os.getenv("RAW_DATA_PATH")
SAVE_PATH = os.getenv("SAVE_DATA_PATH")


def main(data_path, engine):
    manager = DataManager(data_path, engine)
    manager.run_pipeline()


if __name__ == "__main__":
    main(DATA_PATH, engine=create_engine(SAVE_PATH))  # pragma: no cover
