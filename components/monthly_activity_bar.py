import streamlit as st
import pandas as pd
import plotly.express as px


def monthly_activity_bar(df):

    st.markdown("---")
    st.markdown("### 📊 Evolução Mensal por Tipo de Solicitação")
    st.markdown("""
    Este gráfico de colunas mostra o volume de tarefas criadas a cada mês, agrupadas pelo tipo de solicitação. 
    Use-o para identificar tendências e comparar a carga de trabalho entre diferentes tipos de solicitações ao longo do tempo.
    """)

    if 'TIPO_SOLICITACAO' not in df.columns:
        st.warning("A coluna 'TIPO_SOLICITACAO' não foi encontrada no arquivo para gerar o gráfico de evolução mensal.")
        return

    df_chart = df.copy()
    df_chart['MES_ANO'] = df_chart['CRIADO_EM'].dt.to_period('M').astype(str)

    monthly_activity_counts = df_chart.groupby(['MES_ANO', 'TIPO_SOLICITACAO']).size().reset_index(name='count')

    fig = px.bar(
        monthly_activity_counts,
        x='MES_ANO',
        y='count',
        color='TIPO_SOLICITACAO',  # Usa a coluna correta
        title='Volume Mensal de Tarefas por Tipo de Solicitação',
        labels={'MES_ANO': 'Mês', 'count': 'Número de Tarefas', 'TIPO_SOLICITACAO': 'Tipo de Solicitação'},
        # Corrige a legenda
        barmode='group'
    )

    fig.update_layout(
        xaxis_title="Mês de Criação",
        yaxis_title="Quantidade de Tarefas",
        legend_title="Tipo de Solicitação",  # Corrige o título da legenda
        xaxis={'type': 'category'}
    )

    st.plotly_chart(fig, use_container_width=True)