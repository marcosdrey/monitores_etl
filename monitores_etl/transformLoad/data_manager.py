from datetime import datetime
import sqlite3

import pandas as pd

class DataManager:
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = self.__read_file()

    def run_pipeline(self):
        self.__assure_all_products_have_title()
        self.__clean_seller_field()
        self.__transform_review_rating_field()
        self.__transform_review_total_field()
        self.__transform_price_fields(["old_price", "new_price"])
        self.__add_meta_fields()
        self.__save_to_db()

    def __read_file(self):
        return pd.read_json(
            self.data_path,
            dtype={"old_price": "string", "new_price": "string"}
        )

    def __assure_all_products_have_title(self):
        self.data = self.data[~self.data.title.isna()]

    def __clean_seller_field(self):
        self.data.seller = self.data.seller.apply(
            lambda x: x[4:].strip() if isinstance(x, str)
            and x.startswith("Por ") else x
        )

    def __transform_review_rating_field(self):
        self.data.review_rating = self.data.review_rating.astype(float)

    def __transform_review_total_field(self):
        mask = self.data["review_total"].notna()
    
        self.data.loc[mask, "review_total"] = self.data.loc[
            mask, "review_total"
        ].replace(r"[^\d]", "", regex=True)
        self.data.review_total = self.data.review_total.astype("Int64")

    def __transform_price_fields(self, price_fields):
        for field in price_fields:
            self.data[field] = (
                self.data[field]
                .str.replace(".", "", regex=False)
                .astype(float)
            )

    def __add_meta_fields(self):
        self.data['_source'] = "https://lista.mercadolivre.com.br/monitor-gamer"
        self.data['_datetime'] = datetime.now()

    def __save_to_db(self):
        with sqlite3.connect("data/transformed_data.db") as conn:
            self.data.to_sql("monitores", conn, if_exists="replace", index=False)
