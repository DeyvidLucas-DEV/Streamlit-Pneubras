import plotly.express as px
import streamlit as st


def status_pie(df):
    """Renderiza o grafico de pizza com a distribuicao de tarefas por status."""
    status_counts = df["STATUS"].value_counts().reset_index()
    status_counts.columns = ["Status", "Contagem"]
    fig = px.pie(
        status_counts,
        names="Status",
        values="Contagem",
        title="Distribuição por Status",
        hole=0.4,
    )
    st.plotly_chart(fig, use_container_width=True)

