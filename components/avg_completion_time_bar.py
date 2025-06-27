import pandas as pd
import plotly.express as px

def avg_completion_time_bar(df: pd.DataFrame):
    """
    Calcula o tempo médio de conclusão por responsável da Unitec.
    """
    # Lista de membros da Unitec para verificação
    unitec_members = [
        'Lucas Matheus', 'Priscila Coriolano', 'Raphael Marques Martorella',
        'Vitor Andrade', 'Sósthenes Mendonça', 'Deyvid Lucas Amorim',
        'Emerson Ximenes', 'Flavio Emanuel'
    ]

    cols = ['RESPONSAVEL', 'STATUS', 'DATA_CRIACAO', 'DATA_FINALIZACAO']
    if any(c not in df.columns for c in cols) or df.empty:
        return px.bar(title="Dados insuficientes para calcular o tempo médio")

    # 1. Filtrar tarefas concluídas e com data de finalização
    df_completed = df[
        (df['STATUS'] == 'complete') &
        (pd.notna(df['DATA_FINALIZACAO']))
    ].copy()

    if df_completed.empty:
        return px.bar(title="Nenhuma tarefa concluída no período")

    # 2. Calcular o tempo de conclusão em dias
    df_completed['DATA_CRIACAO'] = pd.to_datetime(df_completed['DATA_CRIACAO'])
    df_completed['DATA_FINALIZACAO'] = pd.to_datetime(df_completed['DATA_FINALIZACAO'])
    df_completed['TEMPO_EM_DIAS'] = (df_completed['DATA_FINALIZACAO'] - df_completed['DATA_CRIACAO']).dt.total_seconds() / (24 * 3600)

    # 3. Separar nomes em tarefas de grupo
    df_completed['RESPONSAVEL'] = df_completed['RESPONSAVEL'].astype(str).str.split(r'\s*,\s*')
    df_exploded = df_completed.explode('RESPONSAVEL')
    df_exploded['RESPONSAVEL'] = df_exploded['RESPONSAVEL'].str.strip()

    # 4. A VERIFICAÇÃO: Manter apenas membros da Unitec
    df_unitec_only = df_exploded[df_exploded['RESPONSAVEL'].isin(unitec_members)]

    # 5. Calcular o tempo médio e ordenar
    avg_time = df_unitec_only.groupby('RESPONSAVEL')['TEMPO_EM_DIAS'].mean().sort_values(ascending=False)

    if avg_time.empty:
        return px.bar(title="Nenhum membro da Unitec com tarefas concluídas")

    # 6. Criar o gráfico
    fig = px.bar(
        avg_time,
        x=avg_time.index,
        y=avg_time.values,
        labels={'x': 'Responsável', 'y': 'Tempo Médio (dias)'},
        text=avg_time.values
    )
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    return fig