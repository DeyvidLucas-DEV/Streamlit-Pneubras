import plotly.express as px
import streamlit as st
import pandas as pd



def temporal_area(df):
    """
    Renderiza um gráfico de área mostrando o volume de tarefas criadas ao longo do tempo.
    """
    st.markdown("---")
    st.markdown("### 📈 Evolução Temporal de Tarefas Criadas")
    st.markdown(
        "Acompanhe a criação de novas tarefas ao longo do tempo. Este gráfico de área mostra o volume diário de novas demandas, ajudando a visualizar picos de trabalho.")

    df['DATA_CRIACAO'] = pd.to_datetime(df['CRIADO_EM']).dt.date
    daily_counts = df.groupby('DATA_CRIACAO').size().reset_index(name='count')

    fig = px.area(
        daily_counts,
        x='DATA_CRIACAO',
        y='count',
        title='Volume de Tarefas Criadas por Dia',
        labels={'DATA_CRIACAO': 'Data', 'count': 'Número de Tarefas Criadas'}
    )

    st.plotly_chart(fig, use_container_width=True)

