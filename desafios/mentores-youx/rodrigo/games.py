import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Carregamento de dados
df = pd.read_csv('games.csv')
dados = df
dados_plataforma = ['Todas'] + sorted(dados['plataforma'].unique().tolist())

# Infos
st.set_page_config(layout='wide')

st.title('🎮 Perfil Gamer')
st.write('Dashboard sobre hábitos de jogos digitais.')
st.sidebar.header('Filtros')

# Filtros
filtro_plataforma = st.sidebar.selectbox('Plataforma',dados_plataforma, index=0)
if filtro_plataforma == 'Todas':
    dados_filtrados = dados
else:
    dados_filtrados = dados[dados['plataforma'] == filtro_plataforma]

# Colunas
col1, col2, col3 = st.columns(3)
coll1, coll2 = st.columns(2)

with col1, st.container(border=True):
    st.write('Jogadores')
    st.subheader(len(dados_filtrados))

with col2, st.container(border=True):
    st.write('Horas médias/semana')
    st.subheader(round(dados_filtrados['horas_por_semana'].mean(), 2))

with col3, st.container(border=True):
    st.write('Plataforma dominante')
    plataforma_dominante = dados_filtrados['plataforma'].value_counts().idxmax()
    st.subheader(plataforma_dominante)

# Gráfico "Jogos mais populares"
jogos_populares = (dados_filtrados.groupby('jogo_favorito').size().reset_index(name='quantidade').rename(columns={'jogo_favorito': 'Jogo Favorito', 'quantidade': 'Quantidade'}))

with coll1, st.container(border=True):
    st.subheader('Jogadores mais populares')
    st.bar_chart(jogos_populares, x='Jogo Favorito', y='Quantidade')

horas_media_plataforma = (dados_filtrados.groupby('plataforma')['horas_por_semana'].mean())

with coll2, st.container(border=True):
    st.subheader('Horas médias por plataforma')
    st.bar_chart(horas_media_plataforma)

# DataFrame
st.subheader('Top 5 jogadores mais ativos')
jogadores_mais_ativos = dados_filtrados.sort_values(by='horas_por_semana', ascending=False).head(5)
st.dataframe(jogadores_mais_ativos)