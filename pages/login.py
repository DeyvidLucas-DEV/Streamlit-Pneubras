import os
import requests
import streamlit as st

st.set_page_config(page_title="Login", page_icon="🔒")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

st.title("Autenticação")

with st.form("login_form"):
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    submitted = st.form_submit_button("Entrar")

    if submitted:
        base_url = os.environ.get("API_BASE_URL", st.secrets.get("API_BASE_URL", ""))
        url = f"{base_url}/ad/api/v1/auth/"
        try:
            resp = requests.post(url, json={"username": username, "password": password})
            if resp.status_code == 200:
                data = resp.json()
                if data is True or data.get("response") is True:
                    st.session_state["token"] = data.get("token")
                    st.session_state["authenticated"] = True
                    st.success("Autenticado com sucesso!")
                    st.switch_page("app.py")
                else:
                    st.error("Credenciais inválidas.")
            else:
                st.error("Erro ao autenticar.")
        except Exception:
            st.error("Não foi possível conectar ao servidor de autenticação.")
