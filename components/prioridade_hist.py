import plotly.express as px
import streamlit as st


def prioridade_hist(df):
    """
    Renderiza um histograma da distribuição de tarefas por prioridade.
    """
    st.markdown("---")
    st.markdown("### Prioridade das Tarefas")
    st.markdown(
        "Este histograma ilustra a distribuição das tarefas com base em seu nível de prioridade. Ajuda a entender se a maioria das tarefas é de alta, média ou baixa prioridade.")

    fig = px.histogram(
        df,
        x="PRIORIDADE",
        title="Distribuição de Tarefas por Prioridade",
        category_orders={
            "PRIORIDADE": df["PRIORIDADE"].value_counts().index.tolist()
        },
        labels={'PRIORIDADE': 'Nível de Prioridade'},
    )

    fig.update_layout(
        yaxis_title="Quantidade de Tarefas"
    )

    st.plotly_chart(fig, use_container_width=True)

