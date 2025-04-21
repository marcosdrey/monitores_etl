import os
import sqlite3

from dotenv import load_dotenv

from monitores_etl.transformLoad.main import main

load_dotenv()

MOCK_PATH = os.getenv("TEST_RAW_DATA_PATH")
SAVE_PATH = os.getenv("TEST_SAVE_DATA_PATH")


def test_transformload_main_func(delete_db):
    main(MOCK_PATH, SAVE_PATH)

    assert os.path.exists(SAVE_PATH)
    with sqlite3.connect(SAVE_PATH) as conn:
        result = conn.execute("SELECT COUNT(*) FROM monitores").fetchone()
        assert result[0] > 0
