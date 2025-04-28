import logging
import os
from pathlib import Path

import pytest
from dotenv import load_dotenv
from scrapy.http import Request, TextResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from streamlit.testing.v1.app_test import AppTest
from testcontainers.postgres import PostgresContainer

from monitores_etl.transformLoad.data_manager import DataManager

load_dotenv()

MOCK_PATH = os.getenv("TEST_RAW_DATA_PATH")
SAVE_PATH = os.getenv("TEST_SAVE_DATA_PATH")


@pytest.fixture
def response():
    html_path = Path(__file__).parent / "html_samples" / "default_page.html"
    html = html_path.read_text(encoding="utf-8")
    url = "http://test.com"
    request = Request(url=url)
    return TextResponse(url=url, request=request, body=html, encoding="utf-8")


@pytest.fixture
def expected_data(session):
    manager = DataManager(MOCK_PATH, session.bind)
    manager._transform()
    return manager.data


@pytest.fixture(autouse=True)
def disable_logging():
    logging.getLogger().setLevel(logging.ERROR)


@pytest.fixture
def at():
    return AppTest.from_file("monitores_etl/dashboard/app.py").run()


@pytest.fixture(scope="session")
def engine():
    with PostgresContainer("postgres:16") as postgres:
        postgres.start()
        _engine = create_engine(postgres.get_connection_url())
        yield _engine
        _engine.dispose()


@pytest.fixture
def session(engine):
    _session = sessionmaker(bind=engine)
    session = _session()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
