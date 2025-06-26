import streamlit as st
import oracledb
import pandas as pd
from datetime import datetime  # <-- ADICIONE ESTA LINHA


@st.cache_resource
def init_connection():
    try:
        dsn = oracledb.makedsn(st.secrets["oracle"]["host"], st.secrets["oracle"]["port"],
                               service_name=st.secrets["oracle"]["service_name"])
        connection = oracledb.connect(user=st.secrets["oracle"]["user"], password=st.secrets["oracle"]["password"],
                                      dsn=dsn)
        return connection
    except oracledb.Error as e:
        st.error(f"Erro ao conectar ao Oracle DB: {e}")
        return None


@st.cache_data
def run_query(start_date: datetime, end_date: datetime) -> pd.DataFrame:
    conn = init_connection()
    if conn:
        try:
            colunas_necessarias = "STATUS, CRIADO_EM, ATUALIZADO_EM, FECHADO_EM, CONCLUIDO_EM, PRIORIDADE, RESPONSAVEIS, TIPO_SOLICITACAO, NOME"

            query = f"""
                SELECT {colunas_necessarias}
                FROM ad_tarefasclickup
                WHERE CRIADO_EM BETWEEN :start_d AND :end_d
            """

            params = {'start_d': start_date, 'end_d': end_date}

            df = pd.read_sql(query, conn, params=params)

            def convert_lob_to_str(val):
                if hasattr(val, 'read'): return val.read()
                return val

            for col in df.select_dtypes(include=['object']).columns:
                if 'DATA' not in col: df[col] = df[col].apply(convert_lob_to_str)

            rename_map = {
                'CRIADO_EM': 'DATA_CRIACAO', 'ATUALIZADO_EM': 'DATA_ATUALIZACAO',
                'FECHADO_EM': 'DATA_FECHAMENTO', 'CONCLUIDO_EM': 'DATA_CONCLUSAO',
                'RESPONSAVEIS': 'RESPONSAVEL'
            }
            df.rename(columns=rename_map, inplace=True)

            date_cols_to_convert = [col for col in df.columns if 'DATA' in col]
            for col in date_cols_to_convert:
                df[col] = pd.to_datetime(df[col], errors='coerce')

            if 'DATA_CONCLUSAO' in df.columns and 'DATA_CRIACAO' in df.columns:
                df['TEMPO_DECORRIDO_DIAS'] = (df['DATA_CONCLUSAO'] - df['DATA_CRIACAO']).dt.days
            else:
                df['TEMPO_DECORRIDO_DIAS'] = None

            return df
        except Exception as e:
            st.error(f"Erro ao executar a query otimizada: {e}")
            return pd.DataFrame()
    else:
        return pd.DataFrame()