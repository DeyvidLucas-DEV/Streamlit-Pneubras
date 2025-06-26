import os
import pandas as pd
import requests
import streamlit as st

from components.status_pie import status_pie
from components.responsavel_bar import responsavel_bar
from components.monthly_activity_bar import monthly_activity_bar
from components.prioridade_hist import prioridade_hist
from components.avg_completion_time_bar import avg_completion_time_bar
from components.temporal_area import temporal_area

st.set_page_config(page_title="Dashboard IQE", page_icon="📈", layout="wide")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.warning("Faça o login para acessar o dashboard.")
    st.stop()

st.title("Dashboard IQE")

@st.cache_data(show_spinner=False)
def load_data():
    base_url = os.environ.get("API_BASE_URL", st.secrets.get("API_BASE_URL", "http://10.19.10.65:8105"))
    token = st.session_state.get("token", "")
    url = f"{base_url}/api/v1/iqe-data/"
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        return pd.DataFrame(resp.json())
    except Exception as e:
        st.info("Não foi possível obter dados da API, usando arquivo local.")
        return pd.read_csv("TABLE_EXPORT_DATA.csv")

df = load_data()

status_pie(df)
responsavel_bar(df)
monthly_activity_bar(df)
prioridade_hist(df)
avg_completion_time_bar(df)
temporal_area(df)
