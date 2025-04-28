from sqlalchemy.sql import text

from monitores_etl.transformLoad.main import main


def test_transformload_main_func(session, mock_data):
    main(mock_data, session.bind)

    result = session.execute(text("SELECT COUNT(*) FROM monitores")).fetchone()
    assert result[0] > 0
