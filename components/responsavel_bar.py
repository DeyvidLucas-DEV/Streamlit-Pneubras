import plotly.express as px
import streamlit as st


def responsavel_bar(df):
    """Mostra a quantidade de tarefas por responsável em um gráfico de barras."""
    responsaveis_count = df["RESPONSAVEL_UNICO"].value_counts().reset_index()
    responsaveis_count.columns = ["Responsável", "Qtde"]
    fig = px.bar(
        responsaveis_count,
        x="Responsável",
        y="Qtde",
        title="Tarefas por Responsável",
    )
    st.plotly_chart(fig, use_container_width=True)

