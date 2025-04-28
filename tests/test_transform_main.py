import os

from dotenv import load_dotenv
from sqlalchemy.sql import text

from monitores_etl.transformLoad.main import main

load_dotenv()

MOCK_PATH = os.getenv("TEST_RAW_DATA_PATH")
SAVE_PATH = os.getenv("TEST_SAVE_DATA_PATH")


def test_transformload_main_func(session):
    main(MOCK_PATH, session.bind)

    result = session.execute(text("SELECT COUNT(*) FROM monitores")).fetchone()
    assert result[0] > 0
