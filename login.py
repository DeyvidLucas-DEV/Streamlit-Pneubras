import os
import requests
import streamlit as st

# --- Configuração da Página ---
st.set_page_config(page_title="Login", page_icon="🔒")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Se o usuário já estiver autenticado na sessão, redireciona
if st.session_state["authenticated"]:
    st.success("Você já está autenticado!")
    st.switch_page("pages/2_Dashboard_IQE.py")
    st.stop()

st.title("Autenticação de Usuário")

with st.form("login_form"):
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    submitted = st.form_submit_button("Entrar")

    if submitted:
        base_url = os.environ.get("API_BASE_URL", st.secrets.get("API_BASE_URL", "http://10.19.10.65:8105"))
        access_token = os.environ.get("ACCESS_TOKEN", st.secrets.get("ACCESS_TOKEN", ""))

        url = f"{base_url}/ad/api/v1/auth/"
        headers = {}
        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"

        try:
            resp = requests.post(
                url,
                json={"username": username, "password": password},
                headers=headers,
                timeout=10,
            )

            if resp.status_code == 200:
                data = resp.json()
                if data.get("response") is True:
                    # Salva as informações diretamente na sessão
                    st.session_state["token"] = data.get("token")
                    st.session_state["authenticated"] = True
                    st.session_state["user"] = username

                    st.success("Autenticado com sucesso!")
                    st.switch_page("pages/2_Dashboard_IQE.py")
                else:
                    st.error("Credenciais inválidas.")
            else:
                st.error(f"Erro ao autenticar (Código: {resp.status_code}).")
        except requests.exceptions.RequestException as e:
            st.error(f"Não foi possível conectar ao servidor: {e}")