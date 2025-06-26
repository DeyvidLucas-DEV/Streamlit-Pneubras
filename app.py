import streamlit as st

st.set_page_config(
    page_title="Portal de Dashboards - Pneubras",
    page_icon="📊",
    layout="wide"
)

st.title("Portal de Dashboards da Pneubras")
st.sidebar.success("Selecione um dashboard no menu acima.")

st.markdown(
    """
    ### Bem-vindo ao seu portal de análises!

    Utilize o menu na barra lateral à esquerda para navegar entre os dashboards disponíveis.

    **Dashboards Atuais:**
    - **Dashboard IQE:** Análise completa do Índice de Qualidade de Entrega.

    À medida que novos datasets e análises forem adicionados, eles aparecerão como novas opções no menu de navegação.
    """
)

