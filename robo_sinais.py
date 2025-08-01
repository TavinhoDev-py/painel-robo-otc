import pandas as pd
from datetime import datetime

def interpretar_sinal(linha):
    rsi = linha["rsi"]
    macd = linha["macd"]
    macd_signal = linha["macd_signal"]

    if rsi > 70 and macd > macd_signal:
        return "🔴 VENDA"
    elif rsi < 30 and macd < macd_signal:
        return "🟢 COMPRA"
    else:
        return "⚪️ NEUTRO"

def gerar_sinais(df):
    df["sinal"] = df.apply(interpretar_sinal, axis=1)
    return df
