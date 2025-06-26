import plotly.graph_objects as go
import pandas as pd


def status_pie(df: pd.DataFrame):
    fig = go.Figure()

    if df.empty:
        fig.update_layout(
            title_text='Distribuição de Status das Tarefas',
            xaxis_showgrid=False, yaxis_showgrid=False,
            xaxis_visible=False, yaxis_visible=False,
            annotations=[
                dict(text="Não há dados para os filtros selecionados.", xref="paper", yref="paper", showarrow=False,
                     font=dict(size=16))]
        )
    else:
        status_counts = df['STATUS'].value_counts()
        cores_quentes = ['#d32f2f', '#ff7043', '#ffa726', '#ffca28', '#ffeb3b']

        fig.add_trace(go.Pie(
            labels=status_counts.index,
            values=status_counts.values,
            hole=.3,
            marker=dict(colors=cores_quentes, line=dict(color='#ffffff', width=2))
        ))
        fig.update_layout(
            title_text='Distribuição de Status das Tarefas',
            legend_title_text='Status',
            uniformtext_minsize=12,
            uniformtext_mode='hide'
        )

    return fig