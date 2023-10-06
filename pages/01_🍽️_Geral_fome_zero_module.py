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
from folium.plugins import MarkerCluster

from streamlit_folium import folium_static
import inflection

from process_data import clean_data



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

#=============================
# Função para criar mapa

def create_map (df1):
    # Criando o mapa
    map_ = folium.Map( zoom_start=11 )

    #Chamando colunas e DF auxiliar
    columns = ['restaurant_name','city','longitude','latitude','aggregate_rating','address','cuisines','price_type', 'average_cost_for_two','currency','rating_color']

    data = df1.loc[:,columns]
    
    # Criando um cluster de marcadores
    marker_cluster = MarkerCluster().add_to(map_)

    # Adicione marcadores para cada restaurante no DataFrame
    for index, location_info in data.iterrows():
        # Concatene 'average_cost_for_two' e 'currency' na mesma linha
        cost_and_currency = f"{location_info['average_cost_for_two']} - {location_info['currency']}"
        
        # Concatene a classificação com "/5.0" ao valor da classificação
        rating_with_suffix = f"Nota: {location_info['aggregate_rating']}/5.0"
        
        #incluindo as informações no popup
        popup_html = f"<b>Restaurante:</b> {location_info['restaurant_name']}<br>"
        popup_html += f"<b>Cidade:</b> {location_info['city']}<br>"
        popup_html += f"<b>Culinária:</b> {location_info['cuisines']}<br>"
        popup_html += f"{rating_with_suffix}<br>"
        popup_html += f"<b>Média do prato para 2 pessoas:</b> {cost_and_currency}<br>"
        popup_html += f"<b>Endereço:</b> {location_info['address']}"

        # Use a função create_custom_icon para definir o ícone com base na cor da coluna 'rating_color'
        color_icon = create_custom_icon(location_info['rating_color'])
        
        folium.Marker(
            location=[location_info['latitude'], location_info['longitude']],
            popup=folium.Popup(popup_html, max_width=300),
            icon=color_icon
        ).add_to(marker_cluster)
    
    #Ajustar o zoom e a posição do mapa para incluir os marcadores, mapa inicia com zoom próximo aos marcadores   
    map_.fit_bounds(map_.get_bounds(), padding=(100, 100))

    return map_


#=============================
# Função para criar ícone personalizado  no mapa com base na cor
def create_custom_icon(color):
    icon = folium.Icon(color=color)
    return icon



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
    'Brazil', # Variáveis que iniciam no filtro
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
with st.container():
    st.title("Fome Zero!")
    st.subheader ('Encontre seu mais novo restaurante favorito')
    st.markdown('Temos as seguintes marcas dentro da nossa plataforma:')

    restaurants, countries, cities, ratings, cuisines = st.columns(5)
    
    with restaurants:
        # Verificando quantidade de restaurantes cadastrados - Não considerei o nome, somente id
        quant = len(df1["restaurant_id"].unique())
        
        #mostrando as quantidades
        restaurants.metric('Restaurantes Cadastrados',quant)

    with countries:
        # Verificando quantidade de países
        quant = len(df1['country'].unique())
                    
        countries.metric('Paises Cadastrados', quant)
    with cities:
        # Verificando quantidade de cidades
        quant = len(df1["city"].unique())
            
        cities.metric('Cidades Cadastradas', quant)
    
    with ratings:
        # Verificando quantidade de cidades
        quant = df1['votes'].sum()
            
        ratings.metric('Avaliações feitas na plataforma', quant)
    
    with cuisines:
        # Verificando quantidade de culinárias
        quant = len(df1['cuisines'].unique())
            
        cuisines.metric('Tipos de culinária oferecida', quant)        

with st.container():
    st.title("Local dos restaurantes")
    st.dataframe(df1)
    
    #Chamando função para criar mapa
    map_ = create_map(df1)
    
    # Exiba o mapa no Streamlit
    folium_static(map_, width=1366, height=768)
    

