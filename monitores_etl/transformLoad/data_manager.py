import logging
import sqlite3
from datetime import datetime

import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.FileHandler("pipeline.log"), logging.StreamHandler()],
)


class DataManager:
    def __init__(self, data_path, save_path):
        self.data_path = data_path
        self.save_path = save_path
        self.data = self.__read_file()

    def run_pipeline(self):
        logging.info("Iniciando execução da pipeline de dados.")
        self._transform()
        self.__save_to_db()
        logging.info("Pipeline finalizada com sucesso.")

    def _transform(self):
        self.__assure_all_products_have_title()
        self.__clean_seller_field()
        self.__transform_review_rating_field()
        self.__transform_review_total_field()
        self.__transform_price_fields(["old_price", "new_price"])
        self.__add_meta_fields()

    def __read_file(self):
        logging.info(f"Lendo arquivo: {self.data_path}")
        return pd.read_json(
            self.data_path, dtype={"old_price": "string", "new_price": "string"}
        )

    def __assure_all_products_have_title(self):
        initial_count = len(self.data)
        self.data = self.data[~self.data.title.isna()]
        removed = initial_count - len(self.data)
        logging.info(f"Removidos {removed} produtos sem título.")

    def __clean_seller_field(self):
        logging.info("Tratando campo 'seller'.")
        self.data.seller = self.data.seller.apply(
            lambda x: x[4:].strip()
            if isinstance(x, str) and x.startswith("Por ")
            else x
        )

    def __transform_review_rating_field(self):
        logging.info("Convertendo campo 'review_rating' para float.")
        self.data.review_rating = self.data.review_rating.astype(float)

    def __transform_review_total_field(self):
        logging.info("Limpando e tratando campo 'seller'.")
        mask = self.data["review_total"].notna()

        self.data.loc[mask, "review_total"] = self.data.loc[
            mask, "review_total"
        ].replace(r"[^\d]", "", regex=True)
        self.data.review_total = self.data.review_total.astype("Int64")

    def __transform_price_fields(self, price_fields):
        for field in price_fields:
            logging.info(f"Tratando campo {field} e convertendo para float.")
            self.data[field] = (
                self.data[field].str.replace(".", "", regex=False).astype(float)
            )

    def __add_meta_fields(self):
        logging.info("Adicionando campos '_source' e '_datetime'")
        self.data["_source"] = "https://lista.mercadolivre.com.br/monitor-gamer"
        self.data["_datetime"] = datetime.now()

    def __save_to_db(self):
        logging.info("Salvando dados transformados no banco de dados.")
        with sqlite3.connect(self.save_path) as conn:
            self.data.to_sql("monitores", conn, if_exists="replace", index=False)
        logging.info("Dados salvos com sucesso.")
