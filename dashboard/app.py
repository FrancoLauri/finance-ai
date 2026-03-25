import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# cargar .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

st.title("📊 Mis Gastos")

# 🔹 leer datos
query = "SELECT * FROM transactions WHERE status = 'confirmed' ORDER BY id DESC"
df = pd.read_sql(query, engine)

# 🔹 preparar fechas
df["date"] = pd.to_datetime(df["date"])
df["day"] = df["date"].dt.date

# 🔹 filtros UI
col1, col2 = st.columns(2)

with col1:
    time_filter = st.selectbox(
        "📅 Período",
        ["Todo", "Últimos 7 días", "Últimos 30 días"],
        key="time_filter"
    )

with col2:
    categories = df["category"].unique()
    selected_category = st.selectbox(
        "📂 Categoría",
        ["Todas"] + list(categories),
        key="category_filter"
    )

# 🔹 aplicar filtro de tiempo
if time_filter != "Todo":
    today = datetime.today()

    if time_filter == "Últimos 7 días":
        start_date = today - timedelta(days=7)
    elif time_filter == "Últimos 30 días":
        start_date = today - timedelta(days=30)

    df = df[df["date"] >= start_date]

# 🔹 aplicar filtro de categoría
if selected_category != "Todas":
    df = df[df["category"] == selected_category]

# 🔹 total gastado
total = df["amount"].sum()
st.subheader("💰 Total gastado")
st.write(f"## ${total:,.0f}")

# 🔹 evolución temporal
st.write("### 📈 Evolución de gastos")
by_day = df.groupby("day")["amount"].sum()
st.line_chart(by_day)

# 🔹 gastos por categoría
st.write("### 📊 Gastos por categoría")
by_category = df.groupby("category")["amount"].sum().sort_values(ascending=False)
st.bar_chart(by_category)

# 🔹 tabla
st.write("### 📋 Movimientos")
st.dataframe(df.sort_values(by="id", ascending=False))