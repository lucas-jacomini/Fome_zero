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

from utils.process_data import clean_data


#==========================================================================
#FUNÇÕES
#==========================================================================


#-------------------------------------FUNÇÕES DO DASHBOARD--------------------------------------

#=====================================
# Criar cards, mostrando a Cuisine e seu melhor restaurante

def card_cuisines(df1, placement=0):
    
    """
    Esta função é responsável por criar os cards que mostram os principais tipos de culinária, e o melhor restaurante para cada tipo de culinária.
    
    Para chamar a função, precisamos definir o DataFrame e qual o placement.
    'seu_dataframe' - nome do DF utilizado
    'placement'     - número da posição iniciando em 0, onde o primeiro é 0, segundo é 1 e assim por diante. 
                    Exemplo caso queira chamar o 3º colocado, faça <card_cuisines(df1, placement=2)>.
    
    Chamando a função:
    # Substitua 'seu_dataframe' pelo DataFrame que você deseja usar e 'seu_placement' pelo valor desejado para 'placement'.
    # card_cuisines(<seu_dataframe>, placement=<seu_placement>)

    
    """            
    # Cuisine - maior qtdade rest.

    df_cuisine = (df1.loc[:,['cuisines','votes']]
                                                .groupby('cuisines')
                                                .count()
                                                .sort_values('votes', ascending = False)
                                                .reset_index())

    # Filtrando o DF com a cuisine

    filter_cuisine = df_cuisine.iloc[placement,0] #Filtro seleciona a culinária da posição do placement

    filtro = df1['cuisines'].isin([filter_cuisine])
    df_aux = df1.loc[filtro,:]


    # Agrupando restaurantes

    #colunas
    cols = ['country','city','restaurant_name','cuisines','average_cost_for_two', 'aggregate_rating','restaurant_id','currency']

    # ordenando o novo df para mostrar o maior nota e ordendando pelo mais antigo
    df_aux = (df_aux.loc[:,cols]
                        .sort_values(['aggregate_rating','restaurant_id'], ascending=[False, True]) 
                        .reset_index(drop=True)
                        .head(1))


    #Declarando as variáveis
    country = df_aux.iloc[0,0]
    city = df_aux.iloc[0,1]
    restaurant_name = df_aux.iloc[0,2]
    cuisines = df_aux.iloc[0,3]
    average_cost_for_two = df_aux.iloc[0,4]
    aggregate_rating = df_aux.iloc[0,5]
    currency = df_aux.loc[0,'currency']
    
    #criando nova variável para o HELP
    help_input = f'''
    **País**: {country}\n
    **Cidade**: {city}\n
    **Custo médio 2 pessoas**: {average_cost_for_two} - {currency}
    
    '''

    st.metric(f'''**{filter_cuisine}** - {restaurant_name}''',f'{aggregate_rating}/5.0', help=help_input)
    
#=====================================
# Criar A FIG que mostram os top 10, melhores ou piores tipos de culinária.
    
def graf_top_cuisines(df1,asc=False,title = 'Melhores') :
    
    """
    Esta função é responsável por criar A FIG que mostram os top 10, melhores ou piores tipos de culinária.
    
    Para chamar a função, precisamos definir o DataFrame, asc (ascending) e title (título).
    'DataFrame' - nome do DF utilizado - df1
    'asc'       - True (do pior ao melhor, menor ao maior) ou False (maior ao menor, melhor ao pior) 
    'title'     - Título do gráfico, insira entre aspas.    
    Chamando a função:
    # Substitua 'seu_dataframe' pelo DataFrame que você deseja usar e 'asc' por True ou False, é necessário adicionar um <título>.
    # graf_top_cuisines(<seu_dataframe>,asc=<asc>,title = <título>)
    """            
    #Criando DF para calcular os valores
    df_aux = (df1.loc[:,['cuisines','votes','aggregate_rating']]
                                                                .groupby('cuisines')
                                                                .mean()
                                                                .sort_values('aggregate_rating', ascending = asc)#ascending true define os piores e False os melhores.
                                                                .reset_index()
                                                                .head(10)
            )

    fig = px.bar(df_aux,
                x='cuisines', 
                y='aggregate_rating', 
                title = title, 
                text_auto='.2f', 
                color= 'aggregate_rating', 
                color_continuous_scale=  [[0, 'lightblue'], [1, 'darkblue']],
                hover_data='votes',
                labels={
                        'cuisines': 'Culinária',
                        'aggregate_rating': 'Nota',
                        'country': 'País'
                        } )
        # Ajustanto para que os rótulos fiquem fora da figura
    fig = fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        #incluindo contorno nas colunas
    fig = fig.update_traces(marker=dict(line=dict(color='gray', width=1)))
    # Remover a legenda de cores
    fig = fig.update(layout_coloraxis_showscale=False)
    # Removendo o rótulo do eixo Y
    fig = fig.update_yaxes(title_text='Nota')
    #MOSTRANDO GRAFICO
    
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

#Título da página
st.title('Visão Cuisines')
st.subheader('',divider='gray')

with st.container(): #Primeiro container, contendo os 5 cards.

    # st.markdown('Melhores Restaurantes dos Principais tipos Culinários')
    
    st.header('Principais tipos de culinária e o respectivo restaurante com a melhor nota')

    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        
        card_cuisines(df1,placement=0)
            
    with col2:
        # 2 melhor cuisine

       card_cuisines(df1,placement=1)
        
    with col3:
        # 3 melhor cuisine

        card_cuisines(df1,placement=2)
    
    with col4:
        # 4 melhor cuisine

       card_cuisines(df1,placement=3)
    
    with col5:
        # 5 melhor cuisine

        card_cuisines(df1,placement=4)

    st.subheader('',divider='gray')

with st.container():
    #Título do container
    st.header('Top 10 restaurantes')
    #Colunas que serão mostradas
    cols = ['restaurant_id','restaurant_name','country','city','cuisines','average_cost_for_two', 'currency','aggregate_rating']
    #DF para mostrar o Top 10 restaurantes
    df_aux = (df1.loc[:,cols]
                            .sort_values(['aggregate_rating','restaurant_id'], ascending=[False, True]) 
                            .reset_index(drop=True)
                            .head(10))
    st.dataframe(df_aux,) # mostrando o DF
    
    st.subheader('',divider='gray') # separador

with st.container():
    #Título do container
    st.header("Top 10 tipos de Culinárias") # O título está se referindo aos 2 gráficos.
    
    col1, col2 = st.columns(2)
    with col1:
        #10 MELHORES CUISINES   
        fig = graf_top_cuisines(df1,asc=False,title='Melhores')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        #10 PIORES CUISINES
        fig = graf_top_cuisines(df1,asc=True,title='Piores')
        #MOSTRANDO GRAFICO
        st.plotly_chart(fig, use_container_width=True)
