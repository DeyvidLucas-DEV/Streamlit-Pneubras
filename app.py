import streamlit as st
import pandas as pd

from components.status_pie import status_pie
from components.responsavel_bar import responsavel_bar
from components.temporal_area import temporal_area
from components.prioridade_hist import prioridade_hist

st.set_page_config(
    page_title="IQE Dashboard - Pneubras",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_data():
    """Carrega o arquivo CSV e faz o parse das colunas de data."""
    df = pd.read_csv("TABLE_EXPORT_DATA.csv")
    df["CRIADO_EM"] = pd.to_datetime(df["CRIADO_EM"], errors="coerce", dayfirst=True)
    df["ATUALIZADO_EM"] = pd.to_datetime(df["ATUALIZADO_EM"], errors="coerce", dayfirst=True)
    df["FECHADO_EM"] = pd.to_datetime(df["FECHADO_EM"], errors="coerce", dayfirst=True)
    df["CONCLUIDO_EM"] = pd.to_datetime(df["CONCLUIDO_EM"], errors="coerce", dayfirst=True)
    return df


df = load_data()

st.markdown(
    "<h1 style='text-align: center; color: white;'>\ud83d\udcca Índice de Qualidade de Entrega (IQE) - Pneubras</h1>",
    unsafe_allow_html=True,
)
st.markdown("---")

# Sidebar - Filters
with st.sidebar:
    st.header("\ud83d\udd0d Filtros")
    status = st.multiselect(
        "Status",
        df["STATUS"].dropna().unique(),
        default=list(df["STATUS"].dropna().unique()),
    )
    prioridade = st.multiselect(
        "Prioridade",
        df["PRIORIDADE"].dropna().unique(),
        default=list(df["PRIORIDADE"].dropna().unique()),
    )
    responsavel = st.multiselect(
        "Responsável",
        df["RESPONSAVEL_UNICO"].dropna().unique(),
        default=list(df["RESPONSAVEL_UNICO"].dropna().unique()),
    )
    data_min = df["CRIADO_EM"].min()
    data_max = df["CRIADO_EM"].max()
    data_range = st.date_input("Data de Criação", [data_min, data_max])

# Filtering
df_filtered = df[
    df["STATUS"].isin(status)
    & df["PRIORIDADE"].isin(prioridade)
    & df["RESPONSAVEL_UNICO"].isin(responsavel)
    & (df["CRIADO_EM"] >= pd.to_datetime(data_range[0]))
    & (df["CRIADO_EM"] <= pd.to_datetime(data_range[1]))
]

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("\ud83d\udcbe Total de Tarefas", len(df_filtered))
col2.metric("\u2705 Concluídas", (df_filtered["STATUS"] == "complete").sum())
col3.metric("\ud83d\udd50 Abertas", (df_filtered["STATUS"] != "complete").sum())
col4.metric("\ud83d\udc68\u200d\ud83d\udcbb Responsáveis únicos", df_filtered["RESPONSAVEL_UNICO"].nunique())

col_a, col_b = st.columns(2)

with col_a:
    status_pie(df_filtered)

with col_b:
    responsavel_bar(df_filtered)

# Charts displayed full width
temporal_area(df_filtered)
prioridade_hist(df_filtered)

st.markdown("### \ud83d\udcc4 Tabela de Tarefas Filtradas")
st.dataframe(df_filtered)

