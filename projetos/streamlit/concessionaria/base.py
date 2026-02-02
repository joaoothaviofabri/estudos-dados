# importar as bibliotecas]
import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import timedelta

# funções de carregamento de dados
    # Cotações do Itau - ITUB4 - 2010 a 2024
@st.cache_data
def carregar_dados(empresas):
    texto_tickers = " ".join(empresas)
    dados_acao = yf.Tickers(texto_tickers)
    cotacoes_acao = dados_acao.history(start="2023-07-01", end="2024-07-01")
    cotacoes_acao = cotacoes_acao["Close"]
    return cotacoes_acao

@st.cache_data
def carregar_tickers_acoes():
    base_tickers = pd.read_csv("IBOV.csv", sep=";")
    tickers = list(base_tickers["Código"])
    tickers = [item + ".SA" for item in tickers]
    return tickers

acoes = carregar_tickers_acoes()
dados = carregar_dados(acoes)

# criar a interface do streamlit
st.write("""
# App Preço de Ações
O gráfico abaixo representa a evolução do preço das ações ao longo dos anos
""") # markdown

# preparar as vizualizações = filtros
st.sidebar.header("Filtros")

#filtro de acoes
lista_acoes = st.sidebar.multiselect("Escolha as ações para visualizar", dados.columns)
if lista_acoes:
    dados = dados[lista_acoes]
    if len(lista_acoes) == 1:
        acao_unica = lista_acoes[0]
        dados = dados.rename(columns={acao_unica: "Close"})

#filtro de datas
data_inicial = dados.index.min().to_pydatetime()
data_final = dados.index.max().to_pydatetime()
intervalo_data = st.sidebar.slider("Selecione o período", min_value=data_inicial, max_value=data_final, value=(data_inicial, data_final), step=timedelta(days=1))

dados = dados.loc[intervalo_data[0]:intervalo_data[1]]

# criar o gráfico
st.line_chart(dados)

# calculo de performance
texto_performace_ativos = ""

if len(lista_acoes) == 0:
    lista_acoes = list(dados.columns)

elif len(lista_acoes) == 1:
    dados = dados.rename(columns={"Close": acao_unica})


carteira = [1000 for acao in lista_acoes]
total_inicial_carteira = sum(carteira)

for i, acao in enumerate(lista_acoes):
    performace_ativo = dados[acao].iloc[-1] / dados[acao].iloc[0] - 1
    performace_ativo = float(performace_ativo)

    carteira[i] = carteira[i] * (1 + performace_ativo)

    if performace_ativo > 0:
        texto_performace_ativos += f"  \n{acao}: :green[{performace_ativo:.1%}]"

    elif performace_ativo < 0:
        texto_performace_ativos += f"  \n{acao}: :red[{performace_ativo:.1%}]"

    else:
        texto_performace_ativos += f"  \n{acao}: {performace_ativo:.1%}"

total_final_carteira = sum(carteira)
performace_carteira = total_final_carteira / total_inicial_carteira - 1

if performace_carteira > 0:
    texto_performace_carteira = f"Performace da carteira com todos os ativos: :green[{performace_ativo:.1%}]"

elif performace_ativo < 0:
    texto_performace_carteira = f"Performace da carteira com todos os ativos: :red[{performace_ativo:.1%}]"

else:
    texto_performace_carteira = f"Performace da carteira com todos os ativos: {performace_ativo:.1%}"

st.write(f"""
### Performace dos Ativos
Essa foi a performace de cada ativo no período selecionado:

{texto_performace_ativos}

{texto_performace_carteira}
""")