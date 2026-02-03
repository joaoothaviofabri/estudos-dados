# importação de bibliotecas
import streamlit as st
import pandas as pd
import plotly.express as px

# Personalização Geral
st.set_page_config(layout='wide')

# Markdown
st.markdown(
    """
    <style>
    /* Título "Filtro" */
    section[data-testid="stSidebar"] h2 {
        font-size: 56px
    }
    
    /* Texto do multiselect e selectbox */
    section[data-testid="stSidebar"] label {
        font-size: 48px
    }
    </style>
    """,
    unsafe_allow_html=True
)

#carregamento de dados e filtros
df = pd.read_csv('carros.csv')
dados = df.reset_index(drop=True)

dados_marcas = list(dados['marca'].drop_duplicates())
marcas_rename = {marca.upper(): marca for marca in dados_marcas}

dados_info_carros = list(dados.drop(['Unnamed: 0', 'nivel_risco', 'perdas_normalizadas', 'marca', 'numero_portas', 'distancia_eixos', 'comprimento', 'largura', 'altura', 'peso', 'tipo_motor', 'numero_cilindros', 'tamanho_motor', 'diametro_cilindro', 'curso_pistao', 'taxa_compressao', 'potencia', 'rpm_maximo', 'consumo_cidade_mpg', 'consumo_estrada_mpg'], axis=1))

# Rename dos nomes das colunas, legendas e informações das legendas
dados_info_rename = {'tipo_combustivel': 'Tipo de Combustivel', 'aspiracao': 'Aspiração do Motor', 'tipo_carroceria': 'Carroceria', 'tracao': 'Tração', 'local_motor': 'Local do Motor', 'sistema_combustivel': 'Sistema de Injeção', 'preco': 'Preço'}

combustivel_rename = {'gasolina': 'Gasolina', 'diesel': 'Diesel'}

aspiracao_rename = {'padrao': 'Padrão', 'turbo': 'Turbo'}

carroceria_rename = {'sedan': 'Sedan', 'hatchback': 'Hatchback', 'perua': 'Perua', 'conversivel': 'Conversível', 'hardtop': 'Hardtop'}

tracao_rename = {'dianteira': 'Dianteira', 'quatro_por_quatro': 'Tração Integral', 'traseira': 'Traseira'}

local_motor_rename = {'frontal': 'Frontal', 'traseiro': 'Traseiro'}

sistema_injecao_rename = {'4bbl': '4BBL', 'corpo_simples': 'Corpo Simples', 'duplo_corpo': 'Duplo Corpo', 'idi': 'IDI', 'injecao_multiponto': 'Injeção Multiponto', 'injecao_simples': 'Injeção Simples', 'injecao_simples_sequencial': 'Injeção Simples Sequencial', 'mfi': 'MFI'}

filtro_infos_rename = {'tipo_combustivel': combustivel_rename, 'aspiracao': aspiracao_rename, 'tipo_carroceria': carroceria_rename, 'tracao': tracao_rename, 'local_motor': local_motor_rename, 'sistema_combustivel': sistema_injecao_rename}

# Cores padrão do gráfico
cores_padrao = [
    "#1B4F72",
    "#0F67B1",
    "#2E8BC0",
    "#3FA2F6",
    "#96C9F4",
    "#5AB8D6",
    "#7AD1E8",
    "#A1E3D8",
    "#C7EDE6",
    "#FAFFAF"
]

# Título principal
st.markdown(
"<h1 style='text-align: center'>Gráfico de Informações Técnicas de Carros por Marca em Estoque</h1>", unsafe_allow_html=True
)

#  Vizualização - Sidebar
st.header('Filtros')

# Filtro de seleção das Marcas (em upper)
selecao_marcas = st.multiselect('Selecione a marca para vizualizar:', list(marcas_rename.keys()))
selecao_marcas = [marcas_rename[m] for m in selecao_marcas]
if selecao_marcas:
    dados = dados[dados['marca'].isin(selecao_marcas)]

dados['marca'] = dados['marca'].str.upper().str.strip()

# Filtro de vizualização das informações
selecao_info_carro = st.selectbox('Selecione a informação que deseja vizualizar:', [dados_info_rename[col] for col in dados_info_carros])
selecao_info_carro = [col for col, nome in dados_info_rename.items()
                        if nome == selecao_info_carro][0]

# Rename da Legenda
legenda_filtro = dados_info_rename[selecao_info_carro]
dados[legenda_filtro] = dados[selecao_info_carro]

# Rename das informações da Legenda
if selecao_info_carro in filtro_infos_rename:
    dados[legenda_filtro] = dados[selecao_info_carro].map(filtro_infos_rename[selecao_info_carro])
else:
    dados[legenda_filtro] = dados[selecao_info_carro]

# Título do Gráfico
st.markdown(
"<h2 style='text-align: center'>Gráfico de Informações dos Carros em Estoque</h2>", unsafe_allow_html=True
)

# Gráfico de Pizza
if len(selecao_marcas) == 1:
    quantidade_carros_por_marca = (dados.groupby([legenda_filtro]).size().reset_index(name='valores').rename(columns={'valores': 'Valores'}))
    fig_pie = px.pie(quantidade_carros_por_marca, values='Valores', names=legenda_filtro, title=f'Quantidade de carros da marca {selecao_marcas[0].upper()} filtrados por {legenda_filtro.upper()}', hole=0.5, color=legenda_filtro, color_discrete_sequence=cores_padrao)
    fig_pie.update_traces(textinfo='percent+value')
    st.plotly_chart(fig_pie)

# Gráfico de Barra
else:
    quantidade_carros_por_marca = (dados.groupby(['marca', legenda_filtro]).size().reset_index(name='quantidade').rename(columns={'marca': 'Marca', 'quantidade': 'Quantidade de Carro em Estoque'}))
    fig_bar = px.bar(quantidade_carros_por_marca, x='Marca', y='Quantidade de Carro em Estoque', color=legenda_filtro, color_discrete_sequence=cores_padrao, height=500)
    st.plotly_chart(fig_bar, use_container_width=True)