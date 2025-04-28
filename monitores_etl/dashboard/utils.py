import pandas as pd


def load_data_from_db(engine):
    with engine.begin() as conn:
        return pd.read_sql("SELECT * FROM monitores", conn)


def calculate_kpis(df: pd.DataFrame):
    return {
        "total_monitors": df.shape[0],
        "total_brands": df["brand"].nunique(),
        "average_price": df["new_price"].mean(),
        "total_sellers": df["seller"].nunique(),
        "average_rating": df["review_rating"].mean(),
        "average_discount": (100 - (df["new_price"] * 100 / df["old_price"])).mean(),
    }


def count_by_brand(df: pd.DataFrame):
    result = _not_na_brands(df).groupby("brand").size().sort_values(ascending=False)
    return _rename_series(result, "Marca", "Total")


def price_by_brand(df: pd.DataFrame):
    result = round(
        _not_na_brands(df).groupby("brand")["new_price"].mean(), 3
    ).sort_values(ascending=False)
    return _rename_series(result, "Marca", "Preço Médio")


def review_by_brand(df: pd.DataFrame):
    result = round(
        _not_na_brands(df).groupby("brand")["review_rating"].mean(), 3
    ).sort_values(ascending=False)
    return _rename_series(result, "Marca", "Média")


def _not_na_brands(df: pd.DataFrame):
    return df[df["brand"].notna()]


def _rename_series(series: pd.Series, index, column):
    series.index.name = index
    series = series.rename(column)
    return series
