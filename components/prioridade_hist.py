import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


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
        color_map = {
            'nenhuma': '#CFD8DC',
            'high': '#FFF176',
            'urgente': '#FF9800',
            'normal': '#90CAF9'
        }

        fig = px.histogram(
            df.dropna(subset=['PRIORIDADE']),
            x='PRIORIDADE',
            color='PRIORIDADE',
            color_discrete_map=color_map,
            title='Distribuição de Prioridade das Tarefas'
        )
        fig.update_layout(
            xaxis_title='Prioridade',
            yaxis_title='Contagem'
        )

    return fig
