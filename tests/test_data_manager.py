import pandas as pd
from sqlalchemy.sql import text

from monitores_etl.transformLoad.data_manager import DataManager


def test_run_pipeline_creates_database(session, mock_data):
    manager = DataManager(mock_data, session.bind)
    manager.run_pipeline()

    result = session.execute(text("SELECT COUNT(*) FROM monitores")).fetchone()
    assert result[0] > 0


def test_saved_data_is_correct(session, expected_data, mock_data):
    manager = DataManager(mock_data, session.bind)
    manager.run_pipeline()

    result_data = pd.read_sql("SELECT * FROM monitores", session.bind)

    expected_data = expected_data.drop("_datetime", axis=1)
    result_data = result_data.drop("_datetime", axis=1)

    pd.testing.assert_frame_equal(expected_data, result_data, check_dtype=False)
