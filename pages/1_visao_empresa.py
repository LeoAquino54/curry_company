# Importar bibliotecas
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
import PIL.Image as imgpil
import folium
from streamlit_folium import folium_static
#arruma o tamanho dos gráficos
st.set_page_config(page_title='Visão Empresa', page_icon='📊', layout='wide')

def clean_code(df1):
    """ Esta função tem a responsabilidade de limpar o dataframe
    
        Remoção dos dados NaN
        Mudança do tipo da coluna de dados
        Remoção dos espaços das variáveis de texto
        Formatação da coluna de datas
        Limpeza da coluna de tempo (remoção do texto da variável numérica)

        Input: Dataframe
        Output: Dataframe
    """
    # 1. Convertendo a coluna Age de texto para número
    linhas_selecionadas = (df1['Delivery_person_Age'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    linhas_selecionadas = (df1['Road_traffic_density'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    linhas_selecionadas = (df1['Festival'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    linhas_selecionadas = (df1['City'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)
    
    # 2. Convertendo a coluna Ratings de texto para número decimal (float)
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)
    
    # 3. Convertendo a coluna order_date de texto para data
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format="%d-%m-%Y")
    
    # 4. Convertendo multiple_deliveries de texto para número
    linhas_selecionadas = (df1['multiple_deliveries'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)
    
    # 5. Removendo os espaços dentro de strings/texto/object
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    
    # 6. Limpando a coluna de time taken
    df1['Time_taken_min'] = df1['Time_taken(min)'].apply(lambda x: int(x.split('(min) ')[1]))
    df1['Time_taken_min'] = df1['Time_taken_min'].astype(int)

    return df1


def order_metric(df1):
    cols = ['ID', 'Order_Date']
    # Seleção de colunas
    df_aux = df1.loc[:, cols].groupby('Order_Date').count().reset_index()
    # Desenhar o gráfico de linhas
    fig = px.bar(df_aux, x='Order_Date', y='ID')
    return fig 


def traffic_order_share(df1):
    df_aux = df1.loc[:, ['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
    df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN', :]
    df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum()
    fig = px.pie(df_aux, values='entregas_perc', names='Road_traffic_density')
    return fig


def traffic_order_city(df1):
    df_aux = df1.loc[:, ['ID', 'City', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).count().reset_index()
    df_aux = df_aux.loc[df_aux['City'] != 'NaN', :]
    df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN', :]
    fig = px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color='City')
    return fig


def order_by_week(df1):
    df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')
    df_aux = df1.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
    fig = px.line(df_aux, x='week_of_year', y='ID')
    return fig


def order_share_by_week(df1):
    df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')
    df_aux1 = df1.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
    df_aux2 = df1.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby('week_of_year').nunique().reset_index()
    df_aux = pd.merge(df_aux1, df_aux2, how='inner', on='week_of_year')
    df_aux['order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']
    fig = px.line(df_aux, x='week_of_year', y='order_by_deliver')
    return fig


def country_maps(df1):
    df_aux = df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']].groupby(['City', 'Road_traffic_density']).median().reset_index()
    df_aux = df_aux.loc[df_aux['City'] != 'NaN', :]
    df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN', :]
    map = folium.Map()
    for index, location_info in df_aux.iterrows():
        folium.Marker(
            [location_info['Delivery_location_latitude'], location_info['Delivery_location_longitude']]
        ).add_to(map)
    return map


# Importar dataset
df = pd.read_csv('dataset/train.csv')
df = clean_code(df) 
df1 = df.copy()  # Cópia do df para preservar o original

#================================================================================================
# Barra Lateral
#==========================================================================================
st.header("Marketplace - Visão Cliente")

#image_path = 'D:/COMUNIDADE DS/PYTHON INICIANTE/CICLO_5/imgs/abstracte-png.webp'
image = imgpil.open('abstracte-png.webp')
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""____""")
st.sidebar.markdown('## Selecione uma data limite')

date_slider = st.sidebar.slider(
    'Até qual valor?',
    value=datetime(2022, 4, 13),
    min_value=datetime(2022, 2, 11),
    max_value=datetime(2022, 4, 6),
    format='DD-MM-YYYY'
)

traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito',
    ['Low', 'Medium', 'High', 'Jam'],
    default='Low'
)

st.sidebar.markdown("""___""")
st.sidebar.markdown('### Criado por Leonardo Aquino')

# Filtro de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de trânsito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

#================================================================================================
# Layout no Streamlit
#==========================================================================================

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    with st.container():
        # Order Metric
        st.markdown('Orders by Day')
        fig = order_metric(df1)
        st.plotly_chart(fig, use_container_width=True)

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            fig = traffic_order_share(df1)
            st.header("Traffic Order Share")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = traffic_order_city(df1)
            st.header("Traffic Order City")
            st.plotly_chart(fig, use_container_width=True)

with tab2:
    with st.container():
        st.markdown("# Order by Week")
        fig = order_by_week(df1)
        st.plotly_chart(fig, use_container_width=True)

    with st.container():
        st.markdown("# Order Share by Week")
        fig = order_share_by_week(df1)
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.markdown("# Country Maps")
    map = country_maps(df1)
    folium_static(map, width=1024, height=600)
