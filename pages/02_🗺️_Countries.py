# Libraries
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

# bibliotecas necessárias
import folium
import pandas as pd
import streamlit as st
from PIL import Image
from datetime import datetime

from streamlit_folium import folium_static
import inflection

#from utils.process_data import clean_data


#==========================================================================
#FUNÇÕES
#==========================================================================
# FUNÇÕES UTILIZADAS PARA AJUSTE E LIMPEZA DO DF

#=====================================
# Preenchimento do nome dos países

COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
}
def country_name(country_id):
    return COUNTRIES[country_id]

#=====================================
# Criação do Tipo de classe do preço

def create_price_type(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

#=====================================
#Criação do nome das Cores

COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
}
def color_name(color_code):
    return COLORS[color_code]

#=====================================
#Renomear as colunas do DataFrame

def rename_columns(df1):
    df1 = df1.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df1.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df1.columns = cols_new
    return df1

#=====================================
#LIMPANDO DADOS 

def clean_data(file_path): 

    """ Esta função realiza a limpeza da base
    
    """
    
    df1 = pd.read_csv(file_path)

    # Renomeando as colunas do DataFrame - ajustando os nomes.

    df1 = rename_columns(df1)
    
    # Excluindo nan
    df1 = df1.dropna()
    
    # categorizar todos os restaurantes somente por um tipo de culinária
    df1['cuisines'] = df1.loc[:, 'cuisines'].astype(str).apply(lambda x: x.split(',')[0])

    # Substituindo  os nomes dos países e renomeando a coluna
    df1['country'] = df1.loc[:, 'country_code'].apply(lambda x: country_name(x))

    # Criação do Tipo de classe do preço
    df1["price_type"] = df1.loc[:, "price_range"].apply(lambda x: create_price_type(x))
    # Criação do nome das Cores
    df1['color_name'] = df1.loc[:, 'rating_color'].apply(lambda x: color_name(x))

    # Excluindo coluna com somente 1 dado 'switch_to_order_menu'

    df1 = df1.drop('switch_to_order_menu', axis = 1)

    #Excluindo entradas duplicadas

    df1 = df1.drop_duplicates().reset_index(drop=True)

    df1.to_csv("data\processed\data.csv", index=False)


    
    return df1

def adjust_columns_order(dataframe):
    df1 = dataframe.copy()

    new_cols_order = [
        "restaurant_id",
        "restaurant_name",
        "country",
        "city",
        "address",
        "locality",
        "locality_verbose",
        "longitude",
        "latitude",
        "cuisines",
        "price_type",
        "average_cost_for_two",
        "currency",
        "has_table_booking",
        "has_online_delivery",
        "is_delivering_now",
        "aggregate_rating",
        "rating_color",
        "color_name",
        "rating_text",
        "votes",
    ]

    return df1.loc[:, new_cols_order]

#-------------------------------------FUNÇÕES DO DASHBOARD--------------------------------------

#=====================================
#Quantidade de restaurantes por país 

def restaurants_by_country(df1):
    """
    A função é utilizada para criar um gráfico de barras, mostrando a quantidade de restaurantes em cada país.

    Args:
        df1 (dataframe): dataframe utilizado

    Returns:
        fig: retorna o gráfico que será mostrado ao inseri-lo na função do streamlit.
    """
    #Criando novo DF agrupando os restaurantes por país e contando a quantidade.
    df_aux = (df1.loc[:,['country','restaurant_id']]
                .groupby(['country'])
                .count()
                .sort_values('restaurant_id', ascending = False)
                .reset_index())
    
    #imprimindo gráfico
    fig = px.bar(df_aux, 
                x='country', 
                y='restaurant_id', 
                text_auto=True, 
                color= 'restaurant_id', 
                color_continuous_scale=  [[0, 'lightblue'], [1, 'darkblue']],
                labels= {
                    'country':'País',
                    'restaurant_id':'Restaurantes'
                })
    
    # Ajustanto para que os rótulos fiquem fora da figura
    fig = fig.update_traces(textfont_size=12, 
                            textangle=0, 
                            textposition="outside", 
                            cliponaxis=False)
    #incluindo contorno nas colunas
    fig = fig.update_traces(marker=dict(line=dict(color='gray', width=1)))
    # Remover a legenda de cores
    fig = fig.update(layout_coloraxis_showscale=False)
    # Removendo o rótulo dos eixos
    fig = (fig.update_xaxes(title_text=None)
                .update_yaxes(title_text=None))
    return fig


#=====================================
    #Quantidade de cidades por país


def cities_by_country(df1):
    """
    A função é utilizada para criar um gráfico de barras, mostrando a quantidade de cidades que possuem em restaurantes, segregado por país.

    Args:
        df1 (dataframe): dataframe utilizado

    Returns:
        fig: retorna o gráfico que será mostrado ao inseri-lo na função do streamlit.
    """
    #Quantidade de cidades por país
    df_aux = (df1.loc[:,['country','city']]
                                            .groupby(['country'])
                                            .nunique()
                                            .sort_values('city', ascending = False)
                                            .reset_index())

    #imprimindo gráfico
    fig = px.bar(df_aux, 
                 x='country', 
                 y='city', 
                text_auto=True, color= 'city', 
                color_continuous_scale=  [[0, 'lightblue'], [1, 'darkblue']],
                labels= {
                    'country':'País',
                    'city':'Cidades'
                })
   
    # Ajustanto para que os rótulos fiquem fora da figura
    fig = fig.update_traces(textfont_size=12, 
                            textangle=0, 
                            textposition="outside", 
                            cliponaxis=False)
    
    #incluindo contorno nas colunas
    fig = fig.update_traces(marker=dict(line=dict(color='gray', width=1)))
    
    # Remover a legenda de cores
    fig = fig.update(layout_coloraxis_showscale=False)
    
    # Removendo o rótulo dos eixos
    fig = (fig.update_xaxes(title_text=None)
                .update_yaxes(title_text=None))
    
    return fig

#=====================================
#Média de avaliações feitas por país
def votes_by_country (df1):
    
    """
    A função é utilizada para criar um gráfico de barras, mostrando a média de avaliações
    que os restaurantes de cada país possuem.
    

    Args:
        df1 (dataframe): dataframe utilizado

    Returns:
        fig: retorna o gráfico que será mostrado ao inseri-lo na função do streamlit.
    """
    #Média de avaliações feitas por país
    
    df_aux = round(df1.loc[:,['country','votes']]
                                                    .groupby('country')
                                                    .mean()
                                                    .sort_values('votes', ascending= True)
                                                    .reset_index(),2)
    
    #imprimindo Gráfico
    fig = px.bar(df_aux, 
                x='votes', 
                y='country',
                text_auto=True,
                color= 'votes', 
                color_continuous_scale=  [[0, 'lightblue'], [1, 'darkblue']],
                labels= {
                'country':'País',
                'votes':'Avaliações'
                    })
    # Ajustanto para que os rótulos fiquem fora da figura
    fig = fig.update_traces(textfont_size=12, 
                        textangle=0, 
                        textposition="outside", 
                        cliponaxis=False)
        
    # Remover a legenda de cores
    fig = fig.update(layout_coloraxis_showscale=False)
    # Removendo o rótulo do eixo Y
    fig = fig.update_yaxes(title_text=None)

    return fig



#=====================================
# média de preço de um prato para duas pessoas por país
def cost_by_country (df1):
    """
    A função é utilizada para criar um gráfico de barras, mostrando a média do preço
    de um prato para duas pessoas em cada país.    

    Args:
        df1 (dataframe): dataframe utilizado

    Returns:
        fig: retorna o gráfico que será mostrado ao inseri-lo na função do streamlit.
    """      
    df_aux = round(df1.loc[:,['country','average_cost_for_two','currency']]
                                                                    .groupby(['country','currency'])
                                                                    .mean()
                                                                    .sort_values('average_cost_for_two', ascending= True)
                                                                    .reset_index(),2)
    #imprimindo Gráfico
    fig = px.bar(df_aux, 
                x='average_cost_for_two', 
                y='country',
                text_auto=True, 
                color= 'average_cost_for_two', 
                color_continuous_scale=  [[0, 'lightblue'], [1, 'darkblue']],
                labels= {
                'country':'País',
                'average_cost_for_two':'Preço média de prato',
                'currency':'Moeda'
                    })
    
    # Ajustanto para que os rótulos fiquem fora da figura
    fig = fig.update_traces(textfont_size=12, 
                        textangle=0, 
                        textposition="outside", 
                        cliponaxis=False)
    
    # Remover a legenda de cores
    fig = fig.update(layout_coloraxis_showscale=False)
    # Removendo o rótulo do eixo Y
    fig = fig.update_yaxes(title_text=None)
    
    return fig

#*************************************************************************************************************
#===================================== INICIO ESTRUTURA LÓGICA DO CÓDIGO =====================================
#*************************************************************************************************************

#Importando Dataset

RAW_DATA_PATH = r'data/raw_data/zomato.csv'

df1 = clean_data(RAW_DATA_PATH) # Limpando Dataset com função criada.


#=====================================
#Configurações da página
#=====================================
image_path = r'images/logo.png'
image = Image.open( image_path )

st.set_page_config(
    page_title="App Fome Zero",
    page_icon=image,
    layout="wide",
    initial_sidebar_state="expanded"
)


#=====================================
#Barra Lateral
#=====================================

with st.sidebar:

    image_path = r'images/logo.png'
    image = Image.open( image_path )
    st.image( image , width= 120)
    st.divider()
    
    #Seleção para o filtro de países
    st.header('Filtros')
    #Variável
    countries = df1['country'].unique()
    #Criando filtro
    countries_filter = st.multiselect(
    'Escolha os países que deseja visualizar',
    countries, # variáreis selecionáveis
    countries, # Variáveis que iniciam no filtro
    )

    #Filtro por valor
    #Variável
    price = df1['price_type'].unique()
    #Criando filtro
    price_filter = st.multiselect(
    'Escolha os restaurantes pelo preço',
    price, # variáreis selecionáveis
    price, # Variáveis que iniciam no filtro
    )

    #filtro por notas
    #Criando filtro
    rating_filter = st.slider(
    'Ver restaurantes com nota acima de:',
    0.0, # valor inicial
    5.0, # Valor final
    0.0, # valor selecionado
    help='Para não utilizar o filtro, selecione 0.0'
    
    )
    
    st.divider()


    processed_data = pd.read_csv("./data/processed/data.csv")
 
    #BOTÃO PARA DOWNLOAD DA BASE SEM FILTROS
    st.download_button(
        label="Download Data",
        data=processed_data.to_csv(index=False, sep=";"),
        file_name="data.csv",
        mime="text/csv",
    )




#Filtro de paises - filtra o df inteiro conforme a slecção acima
filtro = df1['country'].isin(countries_filter)
df1 = df1.loc[filtro,:]

filtro = df1['price_type'].isin(price_filter)
df1 = df1.loc[filtro,:]

filtro = df1['aggregate_rating'] >= rating_filter
df1 = df1.loc[filtro,:]

#=====================================
#Layout no Streamlit
#=====================================
st.title('Visão Paises')
st.subheader('',divider='gray')

with st.container():
    #Titulo Container
    st.subheader('Quantidade de restaurantes registrados por país')
      
    #Chamando a função
    fig = restaurants_by_country(df1)
    
    #MOSTRANDO GRAFICO
    st.plotly_chart(fig, use_container_width=True)
    
    
    st.subheader('',divider='gray')
with st.container():
    #Titulo Container
    st.subheader('Quantidade de cidades por país')
       
    #Chamando a função
    fig = cities_by_country(df1)
    
    #MOSTRANDO GRAFICO
    st.plotly_chart(fig, use_container_width=True)

    st.subheader('',divider='gray')
with st.container():
    
    col1, col2 = st.columns(2)
        
    with col1:
        
        #Título da Coluna
        st.markdown("<h4 style='text-align: center;'>Quantidade média de avaliações feitas por país</h4>", unsafe_allow_html=True) #utilizado conceitos de função HTML
        
        
        #Chamando a função
        fig = votes_by_country(df1)
        
        #MOSTRANDO GRAFICO
        st.plotly_chart(fig, use_container_width=True)
        
       
    with col2:
        #Título da Coluna
        st.markdown("<h4 style='text-align: center;'>Média de preço de um prato para duas pessoas</h4>", unsafe_allow_html=True) #utilizado conceitos de função HTML
        
        
        #Chamando a função
        fig = cost_by_country(df1)
        

        #MOSTRANDO GRAFICO
        st.plotly_chart(fig, use_container_width=True)
