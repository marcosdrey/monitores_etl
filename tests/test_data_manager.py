import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy.sql import text

from monitores_etl.transformLoad.data_manager import DataManager

load_dotenv()

MOCK_PATH = os.getenv("TEST_RAW_DATA_PATH")
SAVE_PATH = os.getenv("TEST_SAVE_DATA_PATH")


def test_run_pipeline_creates_database(session):
    manager = DataManager(MOCK_PATH, session.bind)
    manager.run_pipeline()

    result = session.execute(text("SELECT COUNT(*) FROM monitores")).fetchone()
    assert result[0] > 0


def test_saved_data_is_correct(session, expected_data):
    manager = DataManager(MOCK_PATH, session.bind)
    manager.run_pipeline()

    result_data = pd.read_sql("SELECT * FROM monitores", session.bind)

    expected_data = expected_data.drop("_datetime", axis=1)
    result_data = result_data.drop("_datetime", axis=1)

    pd.testing.assert_frame_equal(expected_data, result_data, check_dtype=False)
