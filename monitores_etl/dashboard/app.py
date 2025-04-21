import sqlite3

import pandas as pd
import streamlit as st

st.header("📊 Pesquisa - Monitores Gamer no Mercado Livre")

conn = sqlite3.connect("data/transformed_data.db")

data = pd.read_sql("SELECT * FROM monitores", conn)

st.subheader("💡 Principais KPIs")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🖥️ Total de Monitores", value=data.shape[0])

    not_null_brands = data[data["brand"].notna()]
    st.metric("🏷️ Total de Marcas", value=len(not_null_brands.brand.unique()))

with col2:
    average_price = data["new_price"].mean()
    st.metric("💵 Preço Médio (R$)", value=f"{average_price:.2f}")

    not_null_sellers = data[data["seller"].notna()]
    st.metric("🏪 Total de Vendedores", value=len(not_null_sellers.seller.unique()))

with col3:
    average_rating = data["review_rating"].mean()
    st.metric("⭐ Média de Avaliação", value=f"{average_rating:.1f}")

    average_discount = 100 - (data["new_price"] * 100 / data["old_price"])
    st.metric("💵 Média de Desconto (%)", value=f"{average_discount.mean():.2f}")


st.subheader("🔍 Marcas mais encontradas")
col1, col2 = st.columns([4, 2])

with col1:
    count_by_brand = (
        not_null_brands.groupby("brand")["brand"].count().sort_values(ascending=False)
    )
    count_by_brand.index.name = "Marca"
    count_by_brand = count_by_brand.rename("Total")

    col1.bar_chart(count_by_brand, x_label="Marca", y_label="Total")

with col2:
    st.write(count_by_brand)


st.subheader("💵 Preço médio por marca")
col1, col2 = st.columns([4, 2])

with col1:
    price_by_brand = round(
        not_null_brands.groupby("brand")["new_price"].mean(), 3
    ).sort_values(ascending=False)
    price_by_brand.index.name = "Marca"
    price_by_brand = price_by_brand.rename("Preço Médio")

    col1.bar_chart(price_by_brand, x_label="Marca", y_label="Preço Médio")

with col2:
    st.write(price_by_brand)


st.subheader("💡 Satisfação média por marca")
col1, col2 = st.columns([4, 2])

with col1:
    review_by_brand = round(
        not_null_brands.groupby("brand")["review_rating"].mean(), 3
    ).sort_values(ascending=False)
    review_by_brand.index.name = "Marca"
    review_by_brand = review_by_brand.rename("Média")

    col1.bar_chart(review_by_brand, x_label="Marca", y_label="Avaliação Média")

with col2:
    st.write(review_by_brand)

conn.close()
