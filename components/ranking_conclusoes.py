import pandas as pd


def get_ranking_conclusoes(df: pd.DataFrame):

    if df.empty or 'STATUS' not in df.columns or 'RESPONSAVEL' not in df.columns:
        return pd.Series(dtype='int64')

    # Filtra apenas as tarefas com status 'complete'
    df_completed = df[df['STATUS'] == 'complete'].copy()

    if df_completed.empty:
        return pd.Series(dtype='int64')

    # Lógica para contar individualmente tarefas em grupo
    df_completed['RESPONSAVEL'] = df_completed['RESPONSAVEL'].astype(str)
    df_completed['nomes_individuais'] = df_completed['RESPONSAVEL'].str.split(',\s*')
    df_exploded = df_completed.explode('nomes_individuais')
    df_exploded['nomes_individuais'] = df_exploded['nomes_individuais'].str.strip()

    # Conta as ocorrências e pega os 3 maiores
    top_3 = df_exploded['nomes_individuais'].value_counts().nlargest(3)

    return top_3