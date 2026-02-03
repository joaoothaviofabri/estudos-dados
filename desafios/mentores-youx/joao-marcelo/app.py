import streamlit as st
import pandas as pd
import plotly.express as px

try:
    # Título Principal
    st.markdown(
        "<h1 style='text-align center'>Gerador de Gráfico por Arquivo CSV</h1>", unsafe_allow_html=True
    )

    st.markdown(
        "<h4>Carregue um Arquivo CSV para um Gráfico de Linha:</h4>", unsafe_allow_html=True
    )

    arquivo_csv_usuario = st.file_uploader("Carregar Arquivo CSV", type="csv")
    usuario_arquivo_csv = pd.read_csv(arquivo_csv_usuario, index_col=0)
    st.dataframe(usuario_arquivo_csv)

    # Eixo X e Y
    eixo_x = st.selectbox('Escolha o Eixo X:', usuario_arquivo_csv.columns)
    eixo_y = st.selectbox('Escolha o Eixo Y:', usuario_arquivo_csv.columns)

    if arquivo_csv_usuario:
        botao = st.button('Gerar Gráfico Scatter')

        if botao:
            fig = px.scatter(usuario_arquivo_csv, x=eixo_x, y=eixo_y)
            st.plotly_chart(fig)

    # if arquivo_csv_usuario:
    #     botao = st.button('Gerar Gráfico de Histograma  ')

    #     if botao:
    #         fig2 = px.histogram(usuario_arquivo_csv, x='x', y='y')
    #         st.plotly_chart(fig2)

    # if arquivo_csv_usuario:
    #     botao = st.button('Gerar Gráfico de Linha e Histograma  ')

    #     if botao:
    #         fig = px.line(usuario_arquivo_csv, x='x', y='y')
    #         fig2 = px.histogram(usuario_arquivo_csv, x='x', y='y')
    #         st.plotly_chart(fig)
    #         st.plotly_chart(fig2)

except (ValueError):
    st.warning("Carregue um Arquivo CSV antes!")