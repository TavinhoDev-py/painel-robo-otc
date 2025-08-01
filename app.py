import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from robo_sinais import gerar_sinais

st.set_page_config(page_title="Robô de Sinais OTC - 1min", layout="wide")

st.title("📈 Painel de Sinais OTC - Estratégia MHI")
st.caption("Atualização em tempo real baseada em sua planilha Google")

# Autenticar com Google Sheets
escopo = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credenciais = ServiceAccountCredentials.from_json_keyfile_name(
    "creds/planilha-robo-otc-fd948d2f1dce.json", escopo
)
cliente = gspread.authorize(credenciais)

# Acessar planilha
url = "https://docs.google.com/spreadsheets/d/167VZHyZRWbm3fq-uIiZTlyJ8SyPceChwTCgPBbV00ic/edit?usp=drivesdk"
planilha = cliente.open_by_url(url)
aba = planilha.worksheet("Sheet1")  # Altere o nome se sua aba for diferente

# Pegar dados e processar
dados = aba.get_all_records()
df = pd.DataFrame(dados)

if df.empty:
    st.warning("⚠️ Nenhum dado disponível.")
else:
    df["datetime"] = pd.to_datetime(df["datetime"])
    df = gerar_sinais(df)
    df = df.sort_values(by="datetime", ascending=False)

    st.success("✅ Sinais atualizados com sucesso!")
    st.dataframe(df[["datetime", "close", "rsi", "macd", "macd_signal", "sinal"]], use_container_width=True)
