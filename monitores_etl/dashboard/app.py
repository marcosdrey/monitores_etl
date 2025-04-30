import os

import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine

from monitores_etl.dashboard import utils

load_dotenv()


def main(engine):
    st.set_page_config("Dashboard de Monitores", page_icon="🖥️")
    st.header("📊 Pesquisa - Monitores Gamer no Mercado Livre")

    data = utils.load_data_from_db(engine)
    kpis = utils.calculate_kpis(data)

    st.subheader("💡 Principais KPIs")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🖥️ Total de Monitores", value=kpis["total_monitors"])
        st.metric("🏷️ Total de Marcas", value=kpis["total_brands"])

    with col2:
        st.metric("💵 Preço Médio (R$)", value=f"{kpis['average_price']:.2f}")
        st.metric("🏪 Total de Vendedores", value=kpis["total_sellers"])

    with col3:
        st.metric("⭐ Média de Avaliação", value=f"{kpis['average_rating']:.1f}")
        st.metric("💵 Média de Desconto (%)", value=f"{kpis['average_discount']:.2f}")

    st.subheader("🔍 Marcas mais encontradas")
    col1, col2 = st.columns([4, 2])

    with col1:
        count_by_brand = utils.count_by_brand(data)
        col1.bar_chart(count_by_brand, x_label="Marca", y_label="Total")

    with col2:
        st.write(count_by_brand)

    st.subheader("💵 Preço médio por marca")
    col1, col2 = st.columns([4, 2])

    with col1:
        price_by_brand = utils.price_by_brand(data)
        col1.bar_chart(price_by_brand, x_label="Marca", y_label="Preço Médio")

    with col2:
        st.write(price_by_brand)

    st.subheader("💡 Satisfação média por marca")
    col1, col2 = st.columns([4, 2])

    with col1:
        review_by_brand = utils.review_by_brand(data)
        col1.bar_chart(review_by_brand, x_label="Marca", y_label="Avaliação Média")

    with col2:
        st.write(review_by_brand)


if __name__ == "__main__":
    main(engine=create_engine(os.getenv("DATABASE_URL")))
