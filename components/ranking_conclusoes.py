import pandas as pd

def get_ranking_conclusoes(df: pd.DataFrame):
    """
    Calcula os 3 principais responsáveis por tarefas concluídas,
    contando individualmente em tarefas de grupo e verificando se são da Unitec.
    """
    # Lista de membros da Unitec para verificação final
    unitec_members = [
        'Lucas Matheus', 'Priscila Coriolano', 'Raphael Marques Martorella',
        'Vitor Andrade', 'Sósthenes Mendonça', 'Deyvid Lucas Amorim',
        'Emerson Ximenes', 'Flavio Emanuel'
    ]

    if 'RESPONSAVEL' not in df.columns or 'STATUS' not in df.columns or df.empty:
        return pd.Series(dtype='int64')

    # 1. Filtrar apenas tarefas 'complete'
    df_completed = df[df['STATUS'] == 'complete'].copy()
    if df_completed.empty:
        return pd.Series(dtype='int64')

    # 2. Separar nomes em tarefas de grupo
    df_completed['RESPONSAVEL'] = df_completed['RESPONSAVEL'].astype(str).str.split(r'\s*,\s*')
    df_exploded = df_completed.explode('RESPONSAVEL')

    # 3. Remover espaços em branco extras dos nomes
    df_exploded['RESPONSAVEL'] = df_exploded['RESPONSAVEL'].str.strip()

    # 4. A VERIFICAÇÃO: Manter apenas os membros da Unitec na contagem
    df_unitec_only = df_exploded[df_exploded['RESPONSAVEL'].isin(unitec_members)]

    # 5. Calcular o ranking com os dados verificados
    ranking = df_unitec_only['RESPONSAVEL'].value_counts().nlargest(3)

    return ranking