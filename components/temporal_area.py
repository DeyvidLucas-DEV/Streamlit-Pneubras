import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def temporal_area(df: pd.DataFrame):
    fig = go.Figure()
    coluna_data = 'DATA_CRIACAO'

    if df.empty or coluna_data not in df.columns:
        fig.update_layout(
            title_text='Evolução Temporal de Tarefas Criadas',
            xaxis_showgrid=False, yaxis_showgrid=False,
            xaxis_visible=False, yaxis_visible=False,
            annotations=[dict(text="Não há dados para os filtros selecionados.", xref="paper", yref="paper", showarrow=False, font=dict(size=16))]
        )
        return fig

    df_chart = df.copy()
    df_chart['DATA_DIA'] = pd.to_datetime(df_chart[coluna_data]).dt.date
    daily_counts = df_chart.groupby('DATA_DIA').size().reset_index(name='count')

    fig = px.area(
        daily_counts,
        x='DATA_DIA',
        y='count',
        title='Volume de Tarefas Criadas por Dia',
        labels={'DATA_DIA': 'Data', 'count': 'Número de Tarefas Criadas'},
        color_discrete_sequence=['rgba(66, 165, 245, 0.4)']
    )

    return fig
