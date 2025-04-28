import os

import pandas as pd
from dotenv import load_dotenv

from monitores_etl.dashboard import utils
from monitores_etl.transformLoad.data_manager import DataManager

load_dotenv()

MOCK_PATH = os.getenv("TEST_RAW_DATA_PATH")


def test_sql_data_is_correctly_loaded(session):
    manager = DataManager(MOCK_PATH, session.bind)
    manager.run_pipeline()

    data = utils.load_data_from_db(session.bind)
    assert isinstance(data, pd.DataFrame)
    assert not data.empty


def test_calculate_kpis(expected_data):
    kpis = utils.calculate_kpis(expected_data)

    expected_result = {
        "total_monitors": 3,
        "total_brands": 1,
        "average_price": 723.3,
        "average_rating": 4.93,
        "average_discount": 15.53,
        "total_sellers": 1,
    }

    assert kpis["total_monitors"] == expected_result["total_monitors"]
    assert kpis["total_brands"] == expected_result["total_brands"]
    assert round(kpis["average_price"], 1) == expected_result["average_price"]
    assert round(kpis["average_rating"], 2) == expected_result["average_rating"]
    assert round(kpis["average_discount"], 2) == expected_result["average_discount"]
    assert kpis["total_sellers"] == expected_result["total_sellers"]


def test_count_by_brand(expected_data):
    count_by_brand = utils.count_by_brand(expected_data)
    expected_series = pd.Series({"AOC": 1}, index=["AOC"])
    expected_series.index.name = "Marca"
    expected_series = expected_series.rename("Total")

    pd.testing.assert_series_equal(count_by_brand, expected_series, check_dtype=False)


def test_price_by_brand(expected_data):
    price_by_brand = utils.price_by_brand(expected_data)
    expected_series = pd.Series({"AOC": 854}, index=["AOC"])
    expected_series.index.name = "Marca"
    expected_series = expected_series.rename("Preço Médio")

    pd.testing.assert_series_equal(price_by_brand, expected_series, check_dtype=False)


def test_review_by_brand(expected_data):
    review_by_brand = utils.review_by_brand(expected_data)
    expected_series = pd.Series({"AOC": 4.9}, index=["AOC"])
    expected_series.index.name = "Marca"
    expected_series = expected_series.rename("Média")

    pd.testing.assert_series_equal(review_by_brand, expected_series, check_dtype=False)
