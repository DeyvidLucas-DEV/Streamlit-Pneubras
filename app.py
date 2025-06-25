
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard Pneubras", layout="wide", initial_sidebar_state="expanded")

# Carregamento e cache dos dados
@st.cache_data
def load_data():
    df = pd.read_csv("TABLE_EXPORT_DATA.csv")
    df["CRIADO_EM"] = pd.to_datetime(df["CRIADO_EM"], errors="coerce", dayfirst=True)
    df["ATUALIZADO_EM"] = pd.to_datetime(df["ATUALIZADO_EM"], errors="coerce", dayfirst=True)
    df["FECHADO_EM"] = pd.to_datetime(df["FECHADO_EM"], errors="coerce", dayfirst=True)
    df["CONCLUIDO_EM"] = pd.to_datetime(df["CONCLUIDO_EM"], errors="coerce", dayfirst=True)
    return df

df = load_data()

# Título
st.markdown("<h1 style='text-align: center; color: white;'>📊 Dashboard Pneubras - Gerenciamento de Tarefas</h1>", unsafe_allow_html=True)
st.markdown("---")

# SIDEBAR - Filtros
with st.sidebar:
    st.header("🔍 Filtros")
    status = st.multiselect("Status", df["STATUS"].dropna().unique(), default=list(df["STATUS"].dropna().unique()))
    prioridade = st.multiselect("Prioridade", df["PRIORIDADE"].dropna().unique(), default=list(df["PRIORIDADE"].dropna().unique()))
    responsavel = st.multiselect("Responsável", df["RESPONSAVEL_UNICO"].dropna().unique(), default=list(df["RESPONSAVEL_UNICO"].dropna().unique()))
    data_min = df["CRIADO_EM"].min()
    data_max = df["CRIADO_EM"].max()
    data_range = st.date_input("Data de Criação", [data_min, data_max])

# FILTRAGEM
df_filtered = df[
    df["STATUS"].isin(status) &
    df["PRIORIDADE"].isin(prioridade) &
    df["RESPONSAVEL_UNICO"].isin(responsavel) &
    (df["CRIADO_EM"] >= pd.to_datetime(data_range[0])) &
    (df["CRIADO_EM"] <= pd.to_datetime(data_range[1]))
]

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("🧾 Total de Tarefas", len(df_filtered))
col2.metric("✅ Concluídas", (df_filtered["STATUS"] == "complete").sum())
col3.metric("🕐 Abertas", (df_filtered["STATUS"] != "complete").sum())
col4.metric("👨‍💼 Responsáveis únicos", df_filtered["RESPONSAVEL_UNICO"].nunique())

# Layout em colunas
col_a, col_b = st.columns(2)

# Gráfico de Pizza - Por Status
with col_a:
    status_counts = df_filtered["STATUS"].value_counts().reset_index()
    status_counts.columns = ["Status", "Contagem"]
    fig_pizza = px.pie(status_counts, names="Status", values="Contagem", title="Distribuição por Status", hole=0.4)
    st.plotly_chart(fig_pizza, use_container_width=True)

# Gráfico de Barras - Por Responsável
with col_b:
    responsaveis_count = df_filtered["RESPONSAVEL_UNICO"].value_counts().reset_index()
    responsaveis_count.columns = ["Responsável", "Qtde"]
    fig_bar = px.bar(responsaveis_count, x="Responsável", y="Qtde", title="Tarefas por Responsável")
    st.plotly_chart(fig_bar, use_container_width=True)

# Gráfico de Área - Evolução Temporal
df_filtered["mes"] = df_filtered["CRIADO_EM"].dt.to_period("M").astype(str)
evolucao = df_filtered.groupby("mes").size().reset_index(name="quantidade")
fig_area = px.area(evolucao, x="mes", y="quantidade", title="Tarefas Criadas por Mês", markers=True)
st.plotly_chart(fig_area, use_container_width=True)

# Gráfico de Colunas - Tarefa por Prioridade
fig_col = px.histogram(df_filtered, x="PRIORIDADE", color="PRIORIDADE", title="Distribuição por Prioridade")
st.plotly_chart(fig_col, use_container_width=True)

# Tabela final
st.markdown("### 📋 Tabela de Tarefas Filtradas")
st.dataframe(df_filtered)
