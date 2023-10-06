import streamlit as st
from PIL import Image


image_path = r'images/logo.png'
image = Image.open( image_path )

st.set_page_config(
    page_title="Home",
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
    
st.title('Fome Zero!')
st.subheader('O Melhor lugar para encontrar seu mais novo restaurante favorito!')

'''
Os dashboards foram criados para que você possa conhecer quais restaurantes estão disponíveis e encontrar um novo lugar fazer suas refeições.

## Como utilizar?

- #### Visão Geral:
    - Cards contendo os números disponíveis de:
        - Restaurantes cadastrados
        - Países em que temos disponibilidade
        - Cidades que possuem restaurantes
        - Avaliações realizadas
        - Tipos únicos de culinárias cadastradas
    - Mapa dos restaurantes cadastrados.
    
    
- #### Visão países:
    - Quantidade de restaurantes por país e em quantas cidades estamos disponíveis.
    - Média de avaliações e preço de pratos.
    

- #### Visão cidades:
    - Cidades com mais restaurantes.
    - Cidades com melhores ou piores restaurantes.
    - Cidades com mais tipos de culinária.
    
    
- #### Visão culinárias:
    - Principais tipos de culinária e o melhor restaurante.
    - 10 melhores restaurantes
    - 10 melhores e piores tipos de culinária

'''
