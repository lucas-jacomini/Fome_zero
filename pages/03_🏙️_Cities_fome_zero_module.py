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
#Cria DF com a quantidade de restaurantes por cidade e país, e traz o id do restaurante mais antigo.

def restaurant_per_city(df1):
    """
    Esta função é responsável por criar o gráfico que mostra as cidades com mais restaurantes.
    
    Para chamar a função, precisamos definir o DataFrame.
    'seu_dataframe' - nome do DF utilizado
    
    Chamando a função:
    # Substitua 'seu_dataframe' pelo DataFrame que você deseja usar.
    # restaurant_per_city(<seu_dataframe>)

    A função irá retornar um fig, que pode ser utilizado diretamente na função de mostrar gráfico do Streamlit
    
    """    
    df_aux = df1.loc[:,['restaurant_id','country', 'city']].groupby(['country','city']).agg(['count','min'])

    # Renomeando colunas
    df_aux.columns=['amount_of_restaurants','oldest_restaurant']

    # reordenando DF
    df_aux = df_aux.sort_values(['amount_of_restaurants', 'oldest_restaurant'], ascending=[False, True]).reset_index().head(10)

    fig = px.bar(df_aux,x='city', y='amount_of_restaurants',
                                                                    text_auto=True, 
                                                                    color= 'country', 
                                                                    color_continuous_scale=  [[0, 'lightblue'], [1, 'darkblue']],
                                                                    labels={
                                                                    'city': 'Cidades',
                                                                    'amount_of_restaurants': 'Quantidade de Restaurantes',
                                                                    'country': 'País'
                                                                    } 
                                                                    )
        # Ajustanto para que os rótulos fiquem fora da figura
    fig = fig.update_traces(textfont_size=12, 
                            textangle=0, 
                            textposition="outside", 
                            cliponaxis=False)
    #incluindo contorno nas colunas
    fig = fig.update_traces(marker=dict(line=dict(color='darkgray', width=1)))
    # Remover a legenda de cores
    fig = fig.update(layout_coloraxis_showscale=False)
    # Removendo o rótulo do eixo Y
    fig = fig.update_yaxes(title_text='Restaurantes')
    return fig



#=====================================
#Gráfico das top 7 cidades com mais restaurantes com média acima de 4 ou abaixo de 2.5

def restaurant_by_rating(df1,filtro='best/worst',title='something'):
    """
    Os gráficos gerados pela função, mostram a quantidade de restaurantes por cidade, que atendem o critério de
    nota acima de 4.0 ou abaixo de 2.5, ficando a escolha através do parametro <filtro>
    
    Retorna um gráfico de barras mostrando as top7 cidades com mais dos melhores ou dos piores restaurantes, 
    com base na classificação agregada.

    Parâmetros:
    df (DataFrame): O DataFrame contendo os dados dos restaurantes.
    filtro (str): 'best' para os restaurantes com nota acima de 4.0 (melhores restaurantes), 'worst' para os restaurantes com notas abaixo de 2.5 ( piores restaurantes ).
    num_results (int): O número de resultados a serem exibidos no gráfico.
    title(str): Título do gráfico
    
    Retorna:
    fig (plotly.graph_objs.Figure): O gráfico de barras.
    
    """
    
    if filtro == 'best':
        filtro = df1['aggregate_rating'] > 4
    elif filtro == 'worst':
        filtro = df1['aggregate_rating'] < 2.5
    
    #CRIANDO NOVO DF
    df_aux = (df1.loc[filtro,['restaurant_id','city','country']]
            .groupby(['country', 'city'])
            .count()
            .sort_values('restaurant_id', ascending = False)
            .reset_index()
            .head(7))

    #criando grafico
    fig = px.bar(df_aux,
                    x='city', 
                    y='restaurant_id', 
                    title = title, 
                    text_auto='.2f', 
                    color= 'country', 
                # color_continuous_scale=  [[0, 'lightblue'], [1, 'darkblue']],
                    labels={
        'city': 'Cidades',
        'restaurant_id': 'Quantidade de Restaurantes',
        'country': 'País'
        }
    )
        # Ajustanto para que os rótulos fiquem fora da figura
    fig = fig.update_traces(textfont_size=12, 
                            textangle=0, 
                            textposition="outside", 
                            cliponaxis=False)
        #incluindo contorno nas colunas
    fig = fig.update_traces(marker=dict(line=dict(color='gray', width=1)))

    # Remover a legenda de cores
    fig.update(layout_coloraxis_showscale=False)
    # Removendo o rótulo do eixo Y
    fig.update_yaxes(title_text='Restaurantes')
    # Centralizar o título
    fig = fig.update_layout(
            title={
                'x': 0.5,  # Defina o valor x como 0,5 para centralizar horizontalmente
                'xanchor': 'center'  # Centralizar horizontalmente
                }
            )
    return fig



#=====================================
#Top 10 cidades com tipos de culinária distintos
def cuisines_by_city(df1):
    """
    Esta função é responsável por criar o gráfico que mostra as cidades com mais tipos de culinária distintos.
    
    Parâmetros:
    df (DataFrame): O DataFrame contendo os dados dos restaurantes.
    
    Retorna:
    fig (plotly.graph_objs.Figure): O gráfico de barras.

    O retorno deve ser utilizado diretamente na função de mostrar gráfico do Streamlit
    """
    
    df_aux = (df1.loc[:,['city','cuisines','country']]
                .groupby(['country', 'city'])
                .nunique()
                .sort_values('cuisines',ascending = False)
                .reset_index()
                .head(10))

    #criando grafico
    fig = px.bar(df_aux,
                x='city', 
                y='cuisines', 
                text_auto=True,
                color= 'country', 
                #color_continuous_scale=  [[0, 'lightblue'], [1, 'darkblue']]
                labels={
            'city': 'Cidades',
            'cuisines': 'Quantidade de Restaurantes',
            'country': 'País'
            }
                )
        # Ajustanto para que os rótulos fiquem fora da figura
    fig = fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    # Removendo o rótulo do eixo Y
    fig = fig.update_yaxes(title_text='Restaurantes')
        #incluindo contorno nas colunas
    fig = fig.update_traces(marker=dict(line=dict(color='gray', width=1)))
    
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
st.title('Visão Cidades')
st.subheader('',divider='gray')

with st.container(): #Primeiro Container
    #Título do container
    st.subheader('Top 10 cidades com mais restaurantes') 
    #Chamando a função para criar o gráfico
    fig = restaurant_per_city(df1)
    #MOSTRANDO GRAFICO
    st.plotly_chart(fig, use_container_width=True)
    
    #Divider para ter melhor separação no dash
    st.subheader('',divider='gray')
    
with st.container():
    #Título do container
    st.subheader('Top 7 cidades com mais restaurantes de média: ')
    #Criando colunas para mostrar 2 gráficos lado a lado.
    col1, col2 = st.columns(2)
        
    with col1:
        #FILTRANDO REST. ACIMA DE 4

        #Chamando função
        fig = restaurant_by_rating(df1,filtro='best',title='Acima de 4.0')
        
        #MOSTRANDO GRAFICO
        st.plotly_chart(fig, use_container_width=True)    
        
            
    with col2:
        #FILTRANDO REST. ABAIXO DE 2.5

        #Chamando função
        fig = restaurant_by_rating(df1,filtro='worst',title='Abaixo de 2.5')
        
        #MOSTRANDO GRAFICO
        st.plotly_chart(fig, use_container_width=True)    
        
    #Divider para ter melhor separação no dash
    st.subheader('',divider='gray')   

with st.container():
    #Título do Container
    st.subheader("Top 10 cidades com mais tipos de culinária distintos")
    
    #chamando a função
    fig = cuisines_by_city(df1)
    #MOSTRANDO GRAFICO
    st.plotly_chart(fig, use_container_width=True)
    
    
    


