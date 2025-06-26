# Índice de Qualidade de Entrega (IQE)

Dashboard interativo da Pneubras desenvolvido em [Streamlit](https://streamlit.io) para acompanhamento das tarefas do time. Os gráficos foram organizados em componentes individuais para facilitar a manutenção e reutilização.

## Como executar

```bash
pip install -r requirements.txt
streamlit run 2_Dashboard_IQE.py
```

Ao abrir o aplicativo utilize a opção **Login** da barra lateral para se autenticar. O dashboard só é exibido para usuários logados.

## Estrutura do projeto

- `app.py` &mdash; aplicação principal do Streamlit.
- `2_Dashboard_IQE.py` &mdash; página do dashboard IQE (requer login).
- `components/` &mdash; módulos contendo cada gráfico do dashboard.
- `assets/logo/` &mdash; pasta reservada para a logo da Pneubras.
- `TABLE_EXPORT_DATA.csv` &mdash; base de dados utilizada pelo dashboard.

## Gráficos

- **Distribuição por Status**: apresenta em formato de pizza a proporção de tarefas em cada status.
- **Tarefas por Responsável**: gráfico de barras que mostra quantas tarefas estão atribuídas a cada colaborador.
- **Tarefas Criadas por Mês**: gráfico de área exibindo a evolução de criação de tarefas ao longo do tempo.
- **Distribuição por Prioridade**: histograma indicando a quantidade de tarefas por prioridade.

Cada componente possui seu respectivo título e descrição para tornar a apresentação mais clara e profissional.

