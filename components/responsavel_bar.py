import plotly.express as px
import streamlit as st


def responsavel_bar(df):
    """
    Renderiza um gráfico de barras com a contagem de tarefas por responsável.
    """
    st.markdown("### 👨‍💻 Tarefas por Responsável")
    st.markdown(
        "Este gráfico de barras horizontais exibe o número total de tarefas atribuídas a cada responsável, permitindo identificar a carga de trabalho de cada um.")

    responsavel_counts = df["RESPONSAVEL_UNICO"].value_counts().sort_values(ascending=True)

    fig = px.bar(
        x=responsavel_counts.values,
        y=responsavel_counts.index,
        orientation="h",
        title="Contagem de Tarefas por Responsável",
        labels={'x': 'Número de Tarefas', 'y': 'Responsável'},
    )

    st.plotly_chart(fig, use_container_width=True)


