import pandas as pd
import plotly.graph_objects as go


def avg_completion_time_bar(df: pd.DataFrame):
    fig = go.Figure()
    coluna_data_criacao = 'DATA_CRIACAO'
    coluna_data_conclusao = 'DATA_CONCLUSAO'
    coluna_responsavel = 'RESPONSAVEL'
    required_cols = [coluna_data_criacao, coluna_data_conclusao, coluna_responsavel]

    if df.empty or not all(col in df.columns for col in required_cols):
        fig.update_layout(
            title_text='Tempo Médio de Conclusão por Responsável',
            xaxis_showgrid=False, yaxis_showgrid=False,
            xaxis_visible=False, yaxis_visible=False,
            annotations=[
                dict(text="Não há dados para os filtros selecionados.", xref="paper", yref="paper", showarrow=False,
                     font=dict(size=16))]
        )
        return fig

    df_completed = df.dropna(subset=[coluna_data_criacao, coluna_data_conclusao]).copy()

    if df_completed.empty:
        fig.update_layout(
            title_text='Tempo Médio de Conclusão por Responsável',
            xaxis_showgrid=False, yaxis_showgrid=False,
            xaxis_visible=False, yaxis_visible=False,
            annotations=[dict(text="Não há tarefas concluídas para calcular o tempo médio.", xref="paper", yref="paper",
                              showarrow=False, font=dict(size=16))]
        )
        return fig

    df_completed['TEMPO_EM_DIAS'] = (df_completed[coluna_data_conclusao] - df_completed[coluna_data_criacao]).dt.days
    df_completed[coluna_responsavel] = df_completed[coluna_responsavel].astype(str)
    df_completed['nomes_individuais'] = df_completed[coluna_responsavel].str.split(',\s*')
    df_exploded = df_completed.explode('nomes_individuais')
    df_exploded['nomes_individuais'] = df_exploded['nomes_individuais'].str.strip()
    avg_time = df_exploded.groupby('nomes_individuais')['TEMPO_EM_DIAS'].mean().nlargest(10).sort_values()

    fig.add_trace(go.Bar(
        y=avg_time.index,
        x=avg_time.values,
        orientation='h',
        marker_color='#FF8C00'
    ))

    fig.update_layout(
        title='Top 10 - Tempo Médio de Conclusão por Responsável (em Dias)',
        xaxis_title='Dias para Concluir (Média)',
        yaxis_title='Responsável'
    )

    return fig