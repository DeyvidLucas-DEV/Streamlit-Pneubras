# config/auth_manager.py

import streamlit as st
import streamlit_cookies_manager as stc
from datetime import datetime, timedelta
from streamlit_cookies_manager.cookie_manager import CookiesNotReady

# Nomes dos cookies
AUTH_TOKEN_COOKIE = "pneubras_auth_token"
AUTH_USER_COOKIE = "pneubras_auth_user"

# Gerenciador de cookies
cookies = stc.CookieManager()


# (As funções login() e logout() permanecem as mesmas)

def login(token: str, username: str):
    st.session_state["authenticated"] = True
    st.session_state["token"] = token
    st.session_state["user"] = username
    expires_at = datetime.now() + timedelta(hours=1)
    cookies.set(AUTH_TOKEN_COOKIE, token, expires_at=expires_at)
    cookies.set(AUTH_USER_COOKIE, username, expires_at=expires_at)


def logout():
    st.session_state["authenticated"] = False
    if "token" in st.session_state: del st.session_state["token"]
    if "user" in st.session_state: del st.session_state["user"]
    cookies.delete(AUTH_TOKEN_COOKIE)
    cookies.delete(AUTH_USER_COOKIE)


def check_authentication():
    """
    Verifica se o usuário está autenticado, com um mecanismo de segurança
    para evitar loops de recarregamento.
    """
    if st.session_state.get("authenticated"):
        return True

    # --- INÍCIO DA MELHORIA DE ROBUSTEZ ---
    # Inicializa um contador de tentativas na sessão
    if "cookie_retries" not in st.session_state:
        st.session_state.cookie_retries = 0

    try:
        token = cookies.get(AUTH_TOKEN_COOKIE)
        username = cookies.get(AUTH_USER_COOKIE)
        # Se a leitura for bem-sucedida, zera o contador
        st.session_state.cookie_retries = 0
    except CookiesNotReady:
        # Se a leitura falhar, incrementa o contador e tenta recarregar
        st.session_state.cookie_retries += 1

        # Se tentamos mais de 3 vezes sem sucesso, desiste para evitar loop
        if st.session_state.cookie_retries > 3:
            st.error("Não foi possível ler os cookies de autenticação. Tente recarregar a página manualmente (F5).")
            st.stop()  # Para a execução em vez de recarregar de novo

        # Tenta recarregar a página
        st.rerun()
    # --- FIM DA MELHORIA DE ROBUSTEZ ---

    if token and username:
        st.session_state["authenticated"] = True
        st.session_state["token"] = token
        st.session_state["user"] = username
        return True

    return False