import inflection
import pandas as pd

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