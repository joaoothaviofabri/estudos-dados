# importação de bibliotecas
import streamlit as st
import pandas as pd
import numpy as np

#carregamento de dados
df = pd.read_csv('carros.csv')

st.title("Informações Técnicas de Carros - Estoque de Concessionária")

st.sidebar.header("Filtros")