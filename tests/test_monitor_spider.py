from scrapy import Request

from monitores_etl.extraction.extraction.spiders.monitor import MonitorSpider


def test_parser_should_get_3_products(response):
    spider = MonitorSpider()
    total_products = 3

    results = list(spider.parse(response))

    # The list also includes next_page information, so one unit is subtracted
    # from the length of the results
    assert len(results) - 1 == total_products


def test_parser_first_product(response):
    spider = MonitorSpider()

    results = list(spider.parse(response))
    assert results[0] == {
        "title": "Monitor Gamer Alienware 25 360hz Aw2523hf Cor Dark Side "
        "of the Moon 100V/240V",
        "brand": "DELL",
        "seller": "Por Dell ",
        "review_rating": "4.8",
        "review_total": "(187)",
        "old_price": "3.499",
        "new_price": "3.276",
        "page": 1,
    }


def test_parser_next_page(response):
    spider = MonitorSpider()

    results = list(spider.parse(response))
    next_request = results[-1]

    assert isinstance(next_request, Request)
    assert next_request.url == "http://test2.com"
