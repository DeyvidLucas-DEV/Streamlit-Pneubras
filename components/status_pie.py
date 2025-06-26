import plotly.express as px
import streamlit as st


def status_pie(df):
    """
    Renderiza um gráfico de pizza mostrando a distribuição de tarefas por status.
    """
    st.markdown("### Status das Tarefas")
    st.markdown(
        "Este gráfico de pizza mostra a distribuição percentual das tarefas filtradas por status (ex: concluídas, em andamento, etc.).")

    status_counts = df["STATUS"].value_counts()

    fig = px.pie(
        names=status_counts.index,
        values=status_counts.values,
        title="Distribuição de Status das Tarefas",
        hole=0.3,
    )

    fig.update_traces(textinfo="percent+label", pull=[0.05] * len(status_counts.index))
    st.plotly_chart(fig, use_container_width=True)
