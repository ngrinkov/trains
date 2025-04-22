import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

st.set_page_config(page_title="Auto Prices Dashboard", layout="wide", page_icon="🚗")

# Загрузка и очистка данных
@st.cache_data
def load_data():
    df = pd.read_csv("/mount/src/trains/streamlit/Auto_Prices_Economic_Trends_(2019–2023)/automobile_prices_economics_2019_2023.csv") 
    df.columns = df.columns.str.strip()
    df["Month/Year"] = pd.to_datetime(df["Month/Year"], format="%y-%b")
    
    # Использование pd.to_numeric для безопасного преобразования типов
    df["New Price ($)"] = pd.to_numeric(df["New Price ($)"].replace(r'[\$,]', '', regex=True), errors='coerce').fillna(0)
    df["Used Price ($)"] = pd.to_numeric(df["Used Price ($)"].replace(r'[\$,]', '', regex=True), errors='coerce').fillna(0)
    df["Inflation Rate (%)"] = pd.to_numeric(df["Inflation Rate (%)"].str.replace('%', ''), errors='coerce').fillna(0)
    df["Interest Rate (%)"] = pd.to_numeric(df["Interest Rate (%)"].str.replace('%', ''), errors='coerce').fillna(0)
    df["Units Sold"] = pd.to_numeric(df["Units Sold"].str.replace('[,]', '', regex=True), errors='coerce').fillna(0)
    
    df["Year"] = df["Month/Year"].dt.year
    return df

df = load_data()


# --- SIDEBAR ---
st.sidebar.header("📅 Фильтр по дате")
min_date, max_date = df["Month/Year"].min(), df["Month/Year"].max()
date_range = st.sidebar.slider("Период", min_value=min_date, max_value=max_date,
                               value=(min_date, max_date), format="MM.YYYY")

filtered_df = df[(df["Month/Year"] >= date_range[0]) & (df["Month/Year"] <= date_range[1])]

# --- HEADER ---
st.title("🚗 Auto Prices & Economic Trends (2019–2023)")
st.markdown("**Интерактивная аналитика: цены новых и б/у авто, инфляция, процентные ставки и объём продаж.**")

# --- ГРАФИК ЦЕН ---
st.subheader("💰 Динамика цен на автомобили")
fig_price, ax = plt.subplots()
ax.plot(filtered_df["Month/Year"], filtered_df["New Price ($)"], label="Новая цена", color="#1f77b4")
ax.plot(filtered_df["Month/Year"], filtered_df["Used Price ($)"], label="Б/у цена", color="#ff7f0e")
ax.set_ylabel("Цена ($)")
ax.set_xlabel("Дата")
ax.set_title("Цены на новые и подержанные авто")
ax.legend()
st.pyplot(fig_price)

# --- МАКРОЭКОНОМИКА ---
st.subheader("📉 Макроэкономические показатели")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Инфляция**")
    st.line_chart(filtered_df.set_index("Month/Year")["Inflation Rate (%)"])

with col2:
    st.markdown("**Процентная ставка**")
    st.line_chart(filtered_df.set_index("Month/Year")["Interest Rate (%)"])

# --- ПРОДАЖИ ---
st.subheader("🚗 Продажи автомобилей (ед.)")
st.bar_chart(filtered_df.set_index("Month/Year")["Units Sold"])

# --- КОРРЕЛЯЦИЯ ---
st.subheader("📊 Корреляционная матрица")
corr = filtered_df.drop(columns=["Month/Year", "Year"]).corr()
fig_corr, ax = plt.subplots(figsize=(8, 5))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
st.pyplot(fig_corr)

# --- СРЕДНИЕ ЗНАЧЕНИЯ ПО ГОДАМ ---
st.subheader("📅 Сравнение показателей по годам")
yearly = df.groupby("Year")[["New Price ($)", "Used Price ($)", "Inflation Rate (%)",
                             "Interest Rate (%)", "Units Sold"]].mean().round(2)
st.dataframe(yearly)

# --- ТАБЛИЦА ДАННЫХ И СКАЧИВАНИЕ ---
st.subheader("📋 Таблица данных")
st.dataframe(filtered_df)

# Скачать отфильтрованные данные
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Скачать CSV",
    data=csv,
    file_name='filtered_auto_prices.csv',
    mime='text/csv',
)

# --- FOOTER ---
st.markdown("---")
st.markdown("📊 Сделано с ❤️ на Streamlit | Данные: Kaggle (2019–2023)")
