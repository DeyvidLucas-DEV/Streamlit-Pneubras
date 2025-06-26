import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import locale


def monthly_activity_bar(df: pd.DataFrame):
    fig = go.Figure()
    coluna_data = 'DATA_CRIACAO'
    coluna_tipo = 'TIPO_SOLICITACAO'

    if df.empty or coluna_tipo not in df.columns or coluna_data not in df.columns:
        fig.update_layout(
            title_text='Volume Mensal de Tarefas por Tipo de Solicitação',
            xaxis_showgrid=False, yaxis_showgrid=False,
            xaxis_visible=False, yaxis_visible=False,
            annotations=[
                dict(text="Não há dados para os filtros selecionados.", xref="paper", yref="paper", showarrow=False,
                     font=dict(size=16))]
        )
        return fig

    df_chart = df.copy()
    try:
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252')
        except locale.Error:
            pass

    df_chart['MES_ANO_ORDEM'] = df_chart[coluna_data].dt.strftime('%Y-%m')
    df_chart['MES_ANO_LABEL'] = df_chart[coluna_data].dt.strftime('%b - %Y').str.upper()

    monthly_activity_counts = df_chart.groupby(
        ['MES_ANO_ORDEM', 'MES_ANO_LABEL', coluna_tipo]
    ).size().reset_index(name='count')

    monthly_activity_counts.sort_values(by='MES_ANO_ORDEM', inplace=True)

    cores_quentes = ['#d32f2f', '#ff7043', '#ffa726', '#ffca28', '#ffeb3b']

    fig = px.bar(
        monthly_activity_counts,
        x='MES_ANO_LABEL',
        y='count',
        color=coluna_tipo,
        title='Volume Mensal de Tarefas por Tipo de Solicitação',
        labels={'MES_ANO_LABEL': 'Mês de Criação', 'count': 'Quantidade de Tarefas',
                coluna_tipo: 'Tipo de Solicitação'},
        barmode='group',
        color_discrete_sequence=cores_quentes
    )

    fig.update_layout(
        xaxis_title="Mês de Criação",
        yaxis_title="Quantidade de Tarefas",
        legend_title="Tipo de Solicitação",
    )

    return fig