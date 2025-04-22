import streamlit as st
import polars as pl
import altair as alt

st.set_page_config(page_title="🌸 Анализ Iris с Polars", layout="wide")

st.title("🌸 Анализ набора данных Iris с помощью Polars")

# Загружаем файл
df = pl.read_csv("/mount/src/trains/streamlit/iris/iris.csv")

st.subheader("📄 Первые строки данных")
st.dataframe(df.head(10).to_pandas())

# Выбор числовой колонки
numeric_cols = [col for col in df.columns if df[col].dtype in [pl.Float32, pl.Float64]]
col_to_plot = st.selectbox("Выберите числовую колонку для анализа", numeric_cols)

# Выбор вида ириса
species = df["species"].unique().to_list()
selected_species = st.multiselect("Выберите виды для фильтрации", species, default=species)

filtered_df = df.filter(pl.col("species").is_in(selected_species))

# Построение графика
chart = alt.Chart(filtered_df.to_pandas()).mark_bar().encode(
    x=alt.X(f"{col_to_plot}:Q", bin=alt.Bin(maxbins=30)),
    y='count()',
    color='species:N'
).properties(
    width=700,
    height=400,
    title=f"Распределение {col_to_plot} по видам"
)

st.altair_chart(chart, use_container_width=True)
