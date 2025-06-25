import plotly.express as px
import streamlit as st


def temporal_area(df):
    """Exibe a evolução das tarefas ao longo do tempo."""
    df_tmp = df.copy()
    df_tmp["mes"] = df_tmp["CRIADO_EM"].dt.to_period("M").astype(str)
    evolucao = df_tmp.groupby("mes").size().reset_index(name="quantidade")
    fig = px.area(
        evolucao,
        x="mes",
        y="quantidade",
        title="Tarefas Criadas por Mês",
        markers=True,
    )
    st.plotly_chart(fig, use_container_width=True)

