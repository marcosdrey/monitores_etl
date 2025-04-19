# import sqlite3

# import pandas as pd

# monitors_data = pd.read_json("data/raw_data.json", dtype={"old_price": "string", "new_price": "string"})

# # Assegurar que todos os produtos possuam título
# monitors_data = monitors_data[~monitors_data.title.isna()]

# # Remover prefixo 'Por ' e o espaço no final do campo de vendedor.
# monitors_data.seller = monitors_data.seller.apply(
#     lambda x: x[4:].strip() if isinstance(x, str) and x.startswith("Por ") else x
# )

# # Transformar o campo de média de avaliação para o tipo 'float'
# monitors_data.review_rating = monitors_data.review_rating.astype(float)

# # Remover caracteres indesejados do total de avaliações e transformar em inteiro
# mask = monitors_data["review_total"].notna()

# monitors_data.loc[mask, "review_total"] = monitors_data.loc[
#     mask, "review_total"
# ].replace(r"[^\d]", "", regex=True)
# monitors_data.review_total = monitors_data.review_total.astype("Int64")


# # Remover caracteres indesejados dos campos de preços e transformar em float

# monitors_data["old_price"] = (
#     monitors_data["old_price"]
#     .str.replace(".", "", regex=False)
#     .astype(float)
# )


# monitors_data["new_price"] = (
#     monitors_data["new_price"]
#     .str.replace(".", "", regex=False)
#     .astype(float)
# )

# with sqlite3.connect("data/transformed_data.db") as conn:
#     monitors_data.to_sql("monitores", conn, if_exists="replace", index=False)

from data_manager import DataManager

manager = DataManager("data/raw_data.json")
manager.run_pipeline()
