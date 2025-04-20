from pathlib import Path

import pytest
from scrapy.http import Request, TextResponse


@pytest.fixture
def response():
    html_path = Path(__file__).parent / "html_samples" / "default_page.html"
    html = html_path.read_text(encoding="utf-8")
    url = "http://test.com"
    request = Request(url=url)
    return TextResponse(url=url, request=request, body=html, encoding="utf-8")
