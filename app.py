import streamlit as st

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.warning("👋 Por favor, faça o login para continuar.")
    st.info("Acesse a página de 'Login' na barra lateral.")
    st.stop()

with st.sidebar:
    st.write(f"Usuário: {st.session_state.get('user', 'N/A')}")
    if st.button("Logout"):
        st.session_state["authenticated"] = False
        st.session_state["user"] = None
        st.session_state["token"] = None
        st.rerun()

st.title("Bem-vindo ao Dashboard de Análise de Tarefas da Pneubras")
st.markdown("Utilize o menu lateral para navegar entre as páginas.")