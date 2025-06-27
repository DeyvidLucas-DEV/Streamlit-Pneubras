import streamlit as st
import requests
import os

# --- Configuração da Página ---
st.set_page_config(
    page_title="Login - Dashboard Pneubras",
    # Certifique-se de que o caminho para o ícone está correto
    page_icon="assets/logo/pneubras_logo.png",
    layout="centered"
)

def pagina_de_login():
    """
    Renderiza uma página de login com layout aprimorado,
    usando a lógica de autenticação via API endpoint.
    """

    # --- Lógica de Autenticação via API (do seu código original) ---
    def _autenticar_usuario(username, password):
        """Envia as credenciais para o endpoint de autenticação e atualiza a sessão."""
        if not username or not password:
            st.session_state["error"] = "Por favor, preencha o usuário e a senha."
            return

        # Busca a URL base e o token de acesso dos segredos ou variáveis de ambiente
        base_url = os.environ.get("API_BASE_URL", st.secrets.get("API_BASE_URL", "http://10.19.10.65:8105"))
        access_token = os.environ.get("ACCESS_TOKEN", st.secrets.get("ACCESS_TOKEN", ""))

        url = f"{base_url}/ad/api/v1/auth/"
        headers = {}
        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"

        try:
            # Faz a requisição POST para a API de autenticação
            resp = requests.post(
                url,
                json={"username": username, "password": password},
                headers=headers,
                timeout=10,
            )

            # Verifica a resposta da API
            if resp.status_code == 200:
                data = resp.json()
                if data.get("response") is True:
                    # Se a autenticação for bem-sucedida, salva os dados na sessão
                    st.session_state["token"] = data.get("token")
                    st.session_state["authenticated"] = True
                    st.session_state["name"] = username # Salva o nome do usuário
                    if "error" in st.session_state:
                        del st.session_state["error"]
                else:
                    st.session_state["authenticated"] = False
                    st.session_state["error"] = "Credenciais inválidas. Verifique seu usuário e senha."
            else:
                st.session_state["authenticated"] = False
                st.session_state["error"] = f"Erro no servidor de autenticação (Código: {resp.status_code})."

        except requests.exceptions.RequestException as e:
            st.session_state["authenticated"] = False
            st.session_state["error"] = f"Não foi possível conectar ao servidor: {e}"
        except Exception as e:
            st.session_state["authenticated"] = False
            st.session_state["error"] = f"Ocorreu um erro inesperado: {e}"


    # Se o usuário já estiver logado, redireciona para o dashboard
    if st.session_state.get("authenticated", False):
        st.success(f"Login bem-sucedido! Bem-vindo(a), {st.session_state.get('name', '')}.")
        # st.switch_page é a forma recomendada de navegar entre páginas
        st.switch_page("pages/2_Dashboard_IQE.py")

    # --- Estilização com CSS ---
    st.markdown("""
        <style>
            [data-testid="stSidebar"] { display: none; }
            .centered-title { text-align: center; margin-bottom: 25px; font-family: 'Arial', sans-serif; }
            .st-emotion-cache-1y4p8pa { padding-top: 2rem; }
        </style>
    """, unsafe_allow_html=True)

    # --- Layout da Página de Login ---
    col1, col2, col3 = st.columns([1, 1.5, 1])

    with col2:
        try:
            st.image("assets/logo/pneubras_logo.png", use_container_width=True)
        except Exception:
            # Não exibe erro se a logo não for encontrada, para não poluir a interface
            pass

        st.markdown("<h1 class='centered-title'>Portal de Análises</h1>", unsafe_allow_html=True)
        st.caption("Por favor, insira suas credenciais para acessar os dados.")

        with st.container(border=True):
            username = st.text_input(label="👤 Usuário", placeholder="Digite seu nome de usuário")
            password = st.text_input(label="🔑 Senha", placeholder="Digite sua senha", type="password")

            st.write("") # Espaço vertical

            # O botão agora chama a função de autenticação via API
            st.button(
                "Entrar",
                on_click=_autenticar_usuario,
                args=(username, password),
                use_container_width=True,
                type="primary"
            )

        # Exibe mensagens de erro, se houver
        if "error" in st.session_state and st.session_state["error"]:
            st.error(st.session_state["error"])


# --- Execução Principal ---
if __name__ == "__main__":
    pagina_de_login()