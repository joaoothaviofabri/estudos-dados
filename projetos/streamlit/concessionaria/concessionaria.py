# importação de bibliotecas
import streamlit as st
import pandas as pd

# Personalização
st.set_page_config(layout='wide')

#carregamento de dados
df = pd.read_csv('carros.csv')
dados = df.reset_index(drop=True)
dados_marcas = list(dados['marca'].drop_duplicates())
dados_info_carros = list(dados.drop(['Unnamed: 0', 'nivel_risco', 'perdas_normalizadas', 'marca', 'numero_portas', 'distancia_eixos', 'comprimento', 'largura', 'altura', 'peso', 'tipo_motor', 'numero_cilindros', 'tamanho_motor', 'diametro_cilindro', 'curso_pistao', 'taxa_compressao', 'potencia', 'rpm_maximo', 'consumo_cidade_mpg', 'consumo_estrada_mpg'], axis=1))

# Modificação dos nomes das colunas
#dados_info_carros.rename(columns={'tipo_combustivel': 'Tipo de Combustivel', 'aspiracao': 'Aspiração do Motor', 'tipo_carroceria': 'Carroceria', 'tracao': 'Tração', 'local_motor': 'Local do Motor', 'sistema_combustivel': 'Sistema de Injeção', 'preco': 'Preço'}, inplace=True)

st.write("""
# Informações Técnicas de Carros
""")

#  Vizualização - Filtros
st.sidebar.header("Filtros")

# Filtro de seleção das Marcas
selecao_marcas = st.sidebar.multiselect('Selecione a marca para vizualizar', dados_marcas)
if selecao_marcas:
    dados = dados[dados['marca'].isin(selecao_marcas)]

# Filtro de vizualização das informações
selecao_info_carro = st.sidebar.selectbox('Selecione a informação que deseje vizualizar', dados_info_carros)

# Gráfico
quantidade_carros_por_marca = dados.groupby(['marca', selecao_info_carro]).size().reset_index(name='quantidade')
st.bar_chart(quantidade_carros_por_marca, x='marca', x_label='Marca', y='quantidade', y_label='Quantidade', color=selecao_info_carro, height=500, )