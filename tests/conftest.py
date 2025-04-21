import logging
import os
from pathlib import Path

import pytest
from dotenv import load_dotenv
from scrapy.http import Request, TextResponse

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
def delete_db():
    if os.path.exists(SAVE_PATH):
        os.remove(SAVE_PATH)


@pytest.fixture
def expected_data():
    manager = DataManager(MOCK_PATH, SAVE_PATH)
    manager._transform()
    return manager.data


@pytest.fixture(autouse=True)
def disable_logging():
    logging.getLogger().setLevel(logging.ERROR)
