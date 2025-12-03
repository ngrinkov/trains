import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Настройка страницы
st.set_page_config(page_title="Анализ Титаника", layout="wide")

st.title("🚢 Анализ пассажиров Титаника")
st.markdown("Это приложение использует **Streamlit** для анализа выживаемости.")

# 1. Загрузка данных
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    df = pd.read_csv(url)
    return df

df = load_data()

# Показать сырые данные (если пользователь захочет)
if st.checkbox("Показать сырые данные"):
    st.dataframe(df.head(10))

# 2. Боковая панель с фильтрами
st.sidebar.header("Фильтры")

# Фильтр по полу
sex_filter = st.sidebar.multiselect(
    "Выберите пол",
    options=df["Sex"].unique(),
    default=df["Sex"].unique()
)

# Фильтр по классу каюты
class_filter = st.sidebar.multiselect(
    "Выберите класс (Pclass)",
    options=sorted(df["Pclass"].unique()),
    default=sorted(df["Pclass"].unique())
)

# Применяем фильтры к датафрейму
df_selection = df.query(
    "Sex == @sex_filter & Pclass == @class_filter"
)

# Отображаем количество отобранных записей
st.write(f"Найдено записей: **{df_selection.shape[0]}**")

# 3. Основные метрики (KPI)
st.subheader("Общая статистика")
col1, col2, col3 = st.columns(3)

total_passengers = df_selection.shape[0]
survived_passengers = df_selection[df_selection["Survived"] == 1].shape[0]
survival_rate = (survived_passengers / total_passengers * 100) if total_passengers > 0 else 0

col1.metric("Всего пассажиров", total_passengers)
col2.metric("Выжило", survived_passengers)
col3.metric("Процент выживаемости", f"{survival_rate:.2f}%")

st.markdown("---")

# 4. Визуализация
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Выживаемость по полу")
    fig1, ax1 = plt.subplots()
    sns.countplot(data=df_selection, x="Sex", hue="Survived", ax=ax1, palette="pastel")
    ax1.set_title("Кто выжил чаще?")
    ax1.set_ylabel("Количество")
    st.pyplot(fig1)

with col_chart2:
    st.subheader("Распределение возрастов")
    fig2, ax2 = plt.subplots()
    sns.histplot(data=df_selection, x="Age", bins=20, kde=True, ax=ax2, color="orange")
    ax2.set_title("Возраст пассажиров")
    st.pyplot(fig2)