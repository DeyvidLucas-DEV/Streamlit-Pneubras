import streamlit as st
import pandas as pd
import plotly.express as px


def avg_completion_time_bar(df):
    """
    Renderiza um gráfico de barras mostrando o tempo médio de conclusão por tipo de solicitação.
    """
    st.markdown("---")
    st.markdown("### ⏱️ Tempo Médio de Conclusão por Tipo de Solicitação")
    st.markdown("""
    Este gráfico de barras mostra o tempo médio, em dias, para concluir tarefas, agrupado por tipo de solicitação. 
    Ajuda a identificar quais tipos de demanda levam mais tempo para serem resolvidas.
    """)

    if 'TIPO_SOLICITACAO' not in df.columns:
        st.warning("A coluna 'TIPO_SOLICITACAO' é necessária para este gráfico.")
        return

    df_completed = df.dropna(subset=['CRIADO_EM', 'CONCLUIDO_EM']).copy()

    # Converte as colunas para datetime, caso ainda não estejam
    df_completed['CRIADO_EM'] = pd.to_datetime(df_completed['CRIADO_EM'])
    df_completed['CONCLUIDO_EM'] = pd.to_datetime(df_completed['CONCLUIDO_EM'])

    if df_completed.empty:
        st.info("Não há dados de tarefas concluídas com datas válidas para calcular o tempo médio de conclusão.")
        return

    df_completed['DURACAO_DIAS'] = (df_completed['CONCLUIDO_EM'] - df_completed['CRIADO_EM']).dt.days

    avg_time_by_type = df_completed.groupby('TIPO_SOLICITACAO')['DURACAO_DIAS'].mean().sort_values(ascending=False)

    fig = px.bar(
        avg_time_by_type,
        y=avg_time_by_type.index,
        x=avg_time_by_type.values,
        orientation='h',
        title='Tempo Médio de Conclusão (dias) por Tipo de Solicitação',
        labels={'y': 'Tipo de Solicitação', 'x': 'Tempo Médio de Conclusão (dias)'}
    )

    fig.update_layout(
        xaxis_title="Tempo Médio (dias)",
        yaxis_title="Tipo de Solicitação",
        yaxis={'categoryorder': 'total ascending'}
    )

    st.plotly_chart(fig, use_container_width=True)