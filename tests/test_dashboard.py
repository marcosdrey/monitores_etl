def test_app_starts(at):
    assert not at.exception


def test_page_title(at):
    assert len(at.header) == 1
    assert "📊 Pesquisa - Monitores Gamer no Mercado Livre" == at.header[0].value
