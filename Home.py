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
    
st.title('Zomato restaurants Dashboards')
'''
Seja bem vindo ao Dashboard dinâmico da empresa Zomato Restaurants, ps dashboards foram criados para que você possa conhecer quais restaurantes estão disponíveis e encontrar um novo lugar fazer suas refeições.
Estão baseados em 4 visões importantes para o negócio: Geral, Países, Cidades e Culinárias.

## Sobre a Zomato:

A Zomato é um serviço de busca de restaurantes para quem quer sair para jantar, buscar comida ou pedir em casa, com atuação em diversos países da Ásia, Europa e alguns páises na américa, ela foi fundada em julho de 2008 com o intuito de ajudar os clientes a encontrarem restaurantes que atendessem suas necessidades.

## Fonte de dados:

Os dados utilizados são públicos e disponibilizados através da plataforma Kaggle. 
Para o downaload do dataset original, siga o link: https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset?resource=download&select=zomato.csv

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

---

Ajuda - Entre em contao com o responsável:
Discord: lucas.jacomini
Email: lucasjacomini@hotmail.com
LinkedIn: https://www.linkedin.com/in/lucas-ludwig-jacomini/
GitHub: https://github.com/lucas-jacomini
'''
