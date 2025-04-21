from monitores_etl.transformLoad.data_manager import DataManager

DATA_PATH = "data/raw_data.json"
SAVE_PATH = "data/transformed_data.db"


def main(data_path, save_path):
    manager = DataManager(data_path, save_path)
    manager.run_pipeline()


if __name__ == "__main__":
    main(DATA_PATH, SAVE_PATH)  # pragma: no cover
