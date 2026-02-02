# importação de bibliotecas
import streamlit as st
import pandas as pd
import numpy as np

#carregamento de dados
dados = pd.read_csv('carros.csv')
dados_marcas = list(dados['marca'].drop_duplicates())
quantidade_carros_por_marca = dados.groupby('marca')['marca'].count()

st.write("""
# Informações Técnicas de Carros
""")

#  Vizualização - Filtros
st.sidebar.header("Filtros")

# Gráfico 
st.bar_chart(quantidade_carros_por_marca)

# Filtro de vizualização
selecao_marcas = st.sidebar.multiselect('Selecione a marca para vizualizar', dados_marcas)

selecao_info_carro = st.sidebar.multiselect('Selecione a informação que deseje vizualizar', dados_marcas)