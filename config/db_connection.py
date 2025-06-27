import streamlit as st
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, text

@st.cache_resource
def init_connection():
    """
    Inicializa a conexão com o banco de dados usando a engine do SQLAlchemy
    para melhor compatibilidade com o Pandas.
    """
    try:
        # Constrói a URL de conexão a partir dos segredos do Streamlit
        db_url = (
            f"postgresql+psycopg2://{st.secrets['postgres']['user']}:{st.secrets['postgres']['password']}"
            f"@{st.secrets['postgres']['host']}:{st.secrets['postgres']['port']}"
            f"/{st.secrets['postgres']['database']}"
        )
        # Cria a "engine", que gerencia as conexões
        engine = create_engine(db_url)
        return engine
    except Exception as e:
        st.error(f"Erro ao criar a engine do SQLAlchemy: {e}")
        return None

@st.cache_data
def run_query(start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """
    Executa a query no banco de dados usando a engine do SQLAlchemy e retorna um DataFrame.
    """
    engine = init_connection()
    if engine:
        try:
            colunas_necessarias = "STATUS, CRIADO_EM, ATUALIZADO_EM, FECHADO_EM, CONCLUIDO_EM, PRIORIDADE, RESPONSAVEIS, TIPO_SOLICITACAO, NOME"

            # Usar sqlalchemy.text() é uma boa prática para passar parâmetros e evitar SQL Injection
            query = text(f"""
                SELECT {colunas_necessarias}
                FROM tb_oracle.ad_tarefasclickup
                WHERE CRIADO_EM BETWEEN :start_d AND :end_d
            """)

            params = {'start_d': start_date, 'end_d': end_date}

            # O pd.read_sql agora usa a engine, o que resolve o aviso do Pandas
            with engine.connect() as connection:
                df = pd.read_sql(query, connection, params=params)

            # O restante do seu código para processamento de dados continua igual
            df.columns = [col.upper() for col in df.columns]

            def convert_lob_to_str(val):
                if hasattr(val, 'read'):
                    return val.read()
                return val

            for col in df.select_dtypes(include=['object']).columns:
                if 'DATA' not in col:
                    df[col] = df[col].apply(convert_lob_to_str)

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
            st.error(f"Erro ao executar a query com SQLAlchemy: {e}")
            return pd.DataFrame()
    else:
        return pd.DataFrame()