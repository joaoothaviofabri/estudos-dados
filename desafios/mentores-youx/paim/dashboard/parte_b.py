import streamlit as st
import pandas as pd
import numpy as np

df = pd.read_csv('parte_b.csv')
dados = df.drop_duplicates()

soma_casos_acumulados = dados['Casos Acumulados'].sum()

#st.title('Dashzinho (Segundo o Paim)')

#grafico_barra = st.bar_chart(dados, x='UF', y='Município')

st.dataframe(dados[['Casos Acumulados', 'Óbitos Acumulados']])

st.subheader('Top 10 municípios por Casos acumulados')

st.dataframe(dados.groupby('Município')['Casos Acumulados'].sum().sort_values(ascending=False).head(10))

st.subheader('Top 10 por Casos por 100 mil (recalc)')

st.dataframe(dados.groupby('Município')[' Casos por 100 mil (recalc)'].sum().sort_values(ascending=False).head(10))

st.bar_chart(dados, x='UF', y='soma_casos_acumulados')