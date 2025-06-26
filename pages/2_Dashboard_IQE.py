import streamlit as st
import pandas as pd
from datetime import date, datetime

# Verificação de autenticação
if "authenticated" not in st.session_state or not st.session_state.get("authenticated"):
    st.warning("👋 Por favor, faça o login para aceder a este dashboard.")
    st.info("Utilize a página de 'Login' na barra lateral para se autenticar.")
    st.stop()

# Importação dos componentes e da query
from components.status_pie import status_pie
from components.responsavel_bar import responsavel_bar
from components.prioridade_hist import prioridade_hist
from components.monthly_activity_bar import monthly_activity_bar
from components.temporal_area import temporal_area
from components.avg_completion_time_bar import avg_completion_time_bar
from components.ranking_conclusoes import get_ranking_conclusoes
from config.db_connection import run_query

# --- Configuração da Página ---
st.set_page_config(layout="wide", page_title="Dashboard IQE")

# --- Logo e Título Centralizado ---
st.markdown("""
    <style>
    .centered-title { text-align: center; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

col_logo1, col_logo2, col_logo3 = st.columns([1, 0.5, 1])
with col_logo2:
    try:
        st.image("assets/logo/pneubras_logo.png", use_container_width=True)
    except Exception:
        st.warning("Adicione o arquivo 'logo.png' ao projeto para exibir a logo.")

st.markdown("<h1 class='centered-title'>Indice de Qualidade de Entregas (IQE)</h1>", unsafe_allow_html=True)

# --- Lógica de Carregamento e Filtros ---

with st.sidebar:
    st.header('Filtros')

    # Placeholders para os filtros que dependem dos dados
    status_filter_placeholder = st.empty()
    responsavel_filter_placeholder = st.empty()

    # Filtro de data é o primeiro a ser renderizado
    today = date.today()
    start_of_year = datetime(today.year, 1, 1)

    date_filter = st.date_input(
        'Filtrar por Data de Criação',
        value=[start_of_year.date(), today],
        key='date_selector'
    )

if not date_filter or len(date_filter) != 2:
    st.warning("Por favor, selecione um intervalo de datas válido para carregar os dados.")
    st.stop()

start_date, end_date = date_filter

# Chama a query com as datas para carregar os dados de forma otimizada
df = run_query(start_date=datetime.combine(start_date, datetime.min.time()),
               end_date=datetime.combine(end_date, datetime.max.time()))

if df.empty:
    st.warning("Não foram encontrados dados para o período selecionado.")
    st.stop()

# Agora popula os filtros de multiselect com os dados carregados
with st.sidebar:
    # Converte valores para string para evitar erros com None
    status_options = sorted([str(s) for s in df['STATUS'].unique()])
    responsavel_options = sorted([str(r) for r in df['RESPONSAVEL'].unique()])

    status_filter = status_filter_placeholder.multiselect(
        'Filtrar por Status',
        options=status_options,
        default=status_options
    )
    responsavel_filter = responsavel_filter_placeholder.multiselect(
        'Filtrar por Responsável',
        options=responsavel_options,
        default=responsavel_options
    )

# Aplicação dos filtros
df_filtered = df.copy()

# Converte as colunas do DataFrame para string antes de comparar com os filtros
if status_filter:
    df_filtered = df_filtered[df_filtered['STATUS'].astype(str).isin(status_filter)]
if responsavel_filter:
    df_filtered = df_filtered[df_filtered['RESPONSAVEL'].astype(str).isin(responsavel_filter)]

# --- Seção de KPIs Principais ---
total_tarefas = df_filtered.shape[0]
tarefas_concluidas = df_filtered[df_filtered['STATUS'] == 'complete'].shape[0]
percentual_conclusao = (tarefas_concluidas / total_tarefas) * 100 if total_tarefas > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total de Tarefas", f"{total_tarefas}")
col2.metric("Tarefas Concluídas", f"{tarefas_concluidas}")
col3.metric("Taxa de Conclusão", f"{percentual_conclusao:.2f}%")

# --- Ranking Top 3 ---
st.markdown("---")
st.subheader("🏆 Ranking de Performance - Top 3 Conclusões")
st.caption("Os três colaboradores que mais concluíram tarefas no período selecionado.")

top_3_responsaveis = get_ranking_conclusoes(df_filtered)

if not top_3_responsaveis.empty:
    cols_ranking = st.columns(len(top_3_responsaveis))
    medals = ["🥇", "🥈", "🥉"]
    for i, (nome, contagem) in enumerate(top_3_responsaveis.items()):
        with cols_ranking[i]:
            st.metric(label=f"{medals[i]} {nome}", value=f"{contagem} Tarefas Concluídas")
else:
    st.info("Não há dados de conclusão suficientes para gerar o ranking no período selecionado.")

st.markdown("---")

# --- Visualizações (Gráficos) ---
col_graf_1, col_graf_2 = st.columns(2)
with col_graf_1:
    st.subheader("📊 Distribuição de Status das Tarefas")
    st.caption("Visão rápida do fluxo de trabalho através da proporção de tarefas em cada status.")
    st.plotly_chart(status_pie(df_filtered), use_container_width=True)

with col_graf_2:
    st.subheader("🏆 Top 10 Responsáveis por Tarefas")
    st.caption("Exibe os 10 colaboradores com mais tarefas atribuídas (contagem individual).")
    st.plotly_chart(responsavel_bar(df_filtered), use_container_width=True)

col_graf_3, col_graf_4 = st.columns(2)
with col_graf_3:
    st.subheader("🟧 Distribuição de Prioridade")
    st.caption("Histograma que agrupa as tarefas por nível de prioridade.")
    st.plotly_chart(prioridade_hist(df_filtered), use_container_width=True)

with col_graf_4:
    st.subheader("🗓️ Volume Mensal por Tipo de Solicitação")
    st.caption("Compara o volume de tarefas criadas a cada mês, separadas por tipo.")
    st.plotly_chart(monthly_activity_bar(df_filtered), use_container_width=True)

col_graf_5, col_graf_6 = st.columns(2)
with col_graf_5:
    st.subheader("📈 Evolução de Tarefas Criadas")
    st.caption("Gráfico de área que mostra o volume diário de novas tarefas.")
    st.plotly_chart(temporal_area(df_filtered), use_container_width=True)

with col_graf_6:
    st.subheader("⏱️ Tempo Médio de Conclusão")
    st.caption("Ranking do tempo médio (em dias) que os responsáveis levam para concluir uma tarefa.")
    st.plotly_chart(avg_completion_time_bar(df_filtered), use_container_width=True)

# --- Tabela de Dados Detalhada ---
with st.expander("Visualizar dados detalhados"):
    st.dataframe(df_filtered)