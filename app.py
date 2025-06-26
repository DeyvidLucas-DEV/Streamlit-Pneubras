import streamlit as st

st.set_page_config(
    page_title="Portal de Dashboards - Pneubras",
    page_icon="📊",
    layout="wide"
)

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.warning("👋 Por favor, faça o login para aceder aos dashboards.")
    st.info("Utilize a página de 'Login' na barra lateral para se autenticar.")
    st.stop()

st.title("Portal de Dashboards da Pneubras")
st.sidebar.success("Selecione um dashboard no menu acima.")

st.markdown(
    """
    ### Bem-vindo ao seu portal de análises!

    Você está autenticado e pode aceder a todos os recursos.
    """
)