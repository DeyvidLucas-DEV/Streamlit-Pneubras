import streamlit as st
import pandas as pd

# Importando os componentes de visualização
from components.status_pie import status_pie
from components.responsavel_bar import responsavel_bar
from components.temporal_area import temporal_area
from components.prioridade_hist import prioridade_hist
from components.monthly_activity_bar import monthly_activity_bar
from components.avg_completion_time_bar import avg_completion_time_bar

# Configuração da página
st.set_page_config(
    page_title="IQE Dashboard - Pneubras",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --- CARREGAMENTO DOS DADOS ---
@st.cache_data
def load_data():
    """Carrega o arquivo CSV e faz o parse das colunas de data."""
    df = pd.read_csv("TABLE_EXPORT_DATA.csv")
    # Converte colunas de data, tratando erros
    for col in ["CRIADO_EM", "ATUALIZADO_EM", "FECHADO_EM", "CONCLUIDO_EM"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)
    return df


df = load_data()

col1, col2, col3 = st.columns([4, 1, 4]) # ANTES: [3, 2, 3]

with col2:
    try:
        st.image('assets/logo/pneubras_logo.png', use_container_width=True)
    except Exception:
        st.markdown("<p style='text-align: center; color: grey;'><i>Logo não encontrado. Verifique o caminho 'assets/logo/pneubras_logo.png'</i></p>", unsafe_allow_html=True)


st.markdown(
    "<h1 style='text-align: center; color: black;'>📊 Índice de Qualidade de Entrega (IQE) </h1>",
    unsafe_allow_html=True,
)
st.markdown("---")

# --- SIDEBAR E FILTROS ---
with st.sidebar:
    st.header("🔍 Filtros")

    # Filtro por data de criação
    data_min = df["CRIADO_EM"].min().date()
    data_max = df["CRIADO_EM"].max().date()
    data_range = st.date_input("Filtrar por Data de Criação", [data_min, data_max])

    # Filtros multiselect
    status = st.multiselect("Status", df["STATUS"].dropna().unique(), default=list(df["STATUS"].dropna().unique()))
    prioridade = st.multiselect("Prioridade", df["PRIORIDADE"].dropna().unique(),
                                default=list(df["PRIORIDADE"].dropna().unique()))
    responsavel = st.multiselect("Responsável", df["RESPONSAVEL_UNICO"].dropna().unique(),
                                 default=list(df["RESPONSAVEL_UNICO"].dropna().unique()))
    if 'TIPO_SOLICITACAO' in df.columns:
        tipo_solicitacao = st.multiselect("Tipo de Solicitação", df["TIPO_SOLICITACAO"].dropna().unique(),
                                          default=list(df["TIPO_SOLICITACAO"].dropna().unique()))
    else:
        tipo_solicitacao = []

# --- APLICAÇÃO DOS FILTROS ---
start_date = pd.to_datetime(data_range[0])
end_date = pd.to_datetime(data_range[1])
df_filtered = df[(df["CRIADO_EM"] >= start_date) & (df["CRIADO_EM"] <= end_date) & (df["STATUS"].isin(status)) & (
    df["PRIORIDADE"].isin(prioridade)) & (df["RESPONSAVEL_UNICO"].isin(responsavel))]
if 'TIPO_SOLICITACAO' in df.columns and tipo_solicitacao:
    df_filtered = df_filtered[df_filtered["TIPO_SOLICITACAO"].isin(tipo_solicitacao)]

# --- EXIBIÇÃO DO DASHBOARD ---

# KPIs
st.markdown("### 🔢 Métricas Gerais")

# --- Linha 1 de KPIs ---
col1, col2, col3 = st.columns(3)
col1.metric("💾 Total de Tarefas", len(df_filtered))
col2.metric("✅ Concluídas", (df_filtered["STATUS"] == "complete").sum())
col3.metric("🕔 Abertas", (df_filtered["STATUS"] != "complete").sum())

# --- Linha 2 de KPIs (com o novo KPI) ---
df_completed_kpi = df_filtered.dropna(subset=['CRIADO_EM', 'CONCLUIDO_EM'])
if not df_completed_kpi.empty:
    duracao_media = (df_completed_kpi['CONCLUIDO_EM'] - df_completed_kpi['CRIADO_EM']).mean()
    avg_time_str = f"{duracao_media.days}d {duracao_media.seconds // 3600}h"
else:
    avg_time_str = "N/A"

col4, col5, col6 = st.columns(3)
col4.metric("👨‍💻 Responsáveis únicos", df_filtered["RESPONSAVEL_UNICO"].nunique())
col5.metric("⏳ Tempo Médio de Conclusão", avg_time_str)
# col6 está livre para o próximo KPI, como o de SLA.

st.markdown("---")

# Gráficos em colunas
col_a, col_b = st.columns(2)
with col_a:
    status_pie(df_filtered)
with col_b:
    responsavel_bar(df_filtered)

# Gráficos de largura total
temporal_area(df_filtered)
prioridade_hist(df_filtered)
monthly_activity_bar(df_filtered)
avg_completion_time_bar(df_filtered)  # <-- NOVO GRÁFICO

# Tabela de dados
st.markdown("---")
st.markdown("### 📄 Tabela de Tarefas Filtradas")
st.dataframe(df_filtered)