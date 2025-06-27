import pandas as pd
import plotly.express as px

def responsavel_bar(df: pd.DataFrame):
    """
    Cria um gráfico de barras com os top 10 responsáveis por quantidade de tarefas,
    contando individualmente e exibindo apenas membros da Unitec.
    """
    # Lista de membros da Unitec para verificação
    unitec_members = [
        'Lucas Matheus', 'Priscila Coriolano', 'Raphael Marques Martorella',
        'Vitor Andrade', 'Sósthenes Mendonça', 'Deyvid Lucas Amorim',
        'Emerson Ximenes', 'Flavio Emanuel'
    ]

    if 'RESPONSAVEL' not in df.columns or df.empty:
        return px.bar(title="Não há dados de responsáveis para exibir")

    df_copy = df.copy()

    # 1. Separar nomes em tarefas de grupo
    df_copy['RESPONSAVEL'] = df_copy['RESPONSAVEL'].astype(str).str.split(r'\s*,\s*')
    df_exploded = df_copy.explode('RESPONSAVEL')
    df_exploded['RESPONSAVEL'] = df_exploded['RESPONSAVEL'].str.strip()

    # 2. A VERIFICAÇÃO: Filtrar para manter apenas os membros da Unitec
    df_unitec_only = df_exploded[df_exploded['RESPONSAVEL'].isin(unitec_members)]

    # 3. Contar tarefas por responsável verificado
    responsavel_counts = df_unitec_only['RESPONSAVEL'].value_counts().nlargest(10).sort_values(ascending=True)

    if responsavel_counts.empty:
        return px.bar(title="Nenhum membro da Unitec encontrado nos filtros atuais")

    # 4. Criar o gráfico
    fig = px.bar(
        responsavel_counts,
        x=responsavel_counts.values,
        y=responsavel_counts.index,
        orientation='h',
        labels={'x': 'Quantidade de Tarefas', 'y': 'Responsável'},
        text=responsavel_counts.values
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(showlegend=False, yaxis={'categoryorder':'total ascending'})
    return fig