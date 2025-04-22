def test_app_starts(at):
    assert not at.exception


def test_page_title(at):
    assert len(at.header) == 1
    assert "📊 Pesquisa - Monitores Gamer no Mercado Livre" == at.header[0].value


def test_page_subheaders(at):
    assert len(at.subheader) == 4
    assert "💡 Principais KPIs" == at.subheader[0].value
    assert "🔍 Marcas mais encontradas" == at.subheader[1].value
    assert "💵 Preço médio por marca" == at.subheader[2].value
    assert "💡 Satisfação média por marca" == at.subheader[3].value
