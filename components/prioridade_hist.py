import plotly.express as px
import streamlit as st


def prioridade_hist(df):
    """Exibe a distribuição das tarefas por prioridade."""
    fig = px.histogram(
        df,
        x="PRIORIDADE",
        color="PRIORIDADE",
        title="Distribuição por Prioridade",
    )
    st.plotly_chart(fig, use_container_width=True)

