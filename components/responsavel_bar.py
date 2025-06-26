import pandas as pd
import plotly.graph_objects as go


def responsavel_bar(df: pd.DataFrame):
    fig = go.Figure()
    coluna_responsavel = 'RESPONSAVEL'

    if df.empty or coluna_responsavel not in df.columns:
        fig.update_layout(
            title_text='Top 10 Responsáveis por Tarefas',
            xaxis_showgrid=False, yaxis_showgrid=False,
            xaxis_visible=False, yaxis_visible=False,
            annotations=[
                dict(text="Não há dados para os filtros selecionados.", xref="paper", yref="paper", showarrow=False,
                     font=dict(size=16))]
        )
    else:
        df_chart = df.copy()
        df_chart.dropna(subset=[coluna_responsavel], inplace=True)
        df_chart[coluna_responsavel] = df_chart[coluna_responsavel].astype(str)
        df_chart['nomes_individuais'] = df_chart[coluna_responsavel].str.split(',\s*')
        df_exploded = df_chart.explode('nomes_individuais')
        df_exploded['nomes_individuais'] = df_exploded['nomes_individuais'].str.strip()
        responsavel_counts = df_exploded['nomes_individuais'].value_counts().nlargest(10).sort_values()

        fig.add_trace(go.Bar(
            y=responsavel_counts.index,
            x=responsavel_counts.values,
            orientation='h',
            marker_color='#4DB6AC'
        ))
        fig.update_layout(
            title_text='Top 10 Responsáveis por Tarefas (Contagem Individual)',
            xaxis_title='Número de Tarefas Atribuídas',
            yaxis_title='Responsável'
        )

    return fig
