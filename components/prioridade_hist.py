import pandas as pd
import plotly.graph_objects as go


def prioridade_hist(df: pd.DataFrame):
    fig = go.Figure()

    if df.empty or 'PRIORIDADE' not in df.columns:
        fig.update_layout(
            title_text='Distribuição de Prioridade das Tarefas',
            xaxis_showgrid=False, yaxis_showgrid=False,
            xaxis_visible=False, yaxis_visible=False,
            annotations=[
                dict(text="Não há dados para os filtros selecionados.", xref="paper", yref="paper", showarrow=False,
                     font=dict(size=16))]
        )
    else:
        fig.add_trace(go.Histogram(
            x=df['PRIORIDADE'].dropna(),
            name='Prioridade',
            marker_color='#FFA500'
        ))
        fig.update_layout(
            title_text='Distribuição de Prioridade das Tarefas',
            xaxis_title='Prioridade',
            yaxis_title='Contagem'
        )

    return fig