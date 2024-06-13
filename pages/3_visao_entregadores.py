# importar bibliotecas
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

# importar dataset
df = pd.read_csv('dataset/train.csv')

df1 = df.copy()  # copia do df para preservar o original

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
df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(float)

# 3. Convertendo a coluna Order_Date de texto para data
df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format="%d-%m-%Y")

# 4. Convertendo multiple_deliveries de texto para número
linhas_selecionadas = (df1['multiple_deliveries'] != 'NaN ')
df1 = df1.loc[linhas_selecionadas, :].copy()
df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)

# 5. Removendo os espaços dentro de strings/texto/objetos
df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()

# 6. Limpando a coluna de time taken
df1['Time_taken_min'] = df1['Time_taken(min)'].apply(lambda x: int(x.split('(min) ')[1]))
df1['Time_taken_min'] = df1['Time_taken_min'].astype(int)

#================================================================================================
# Barra Lateral
#================================================================================================
st.header("Marketplace - Visão Entregadores")

image_path = 'abstracte-png.webp'
image = imgpil.open(image_path)
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
linhas_selecionadas = df1['Order_Date'] <= date_slider
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de trânsito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

#================================================================================================
# Layout no Streamlit
#================================================================================================

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '', ''])

with tab1:
    with st.container():
        col1, col2, col3, col4 = st.columns(4, gap='large')
        
        with col1:
            maior_idade = df1.loc[:, 'Delivery_person_Age'].max()
            col1.metric('Maior Idade', maior_idade)
        
        with col2:
            menor_idade = df1.loc[:, 'Delivery_person_Age'].min()
            col2.metric('Menor Idade', menor_idade)
        
        with col3:
            melhor_cond = df1.loc[:, 'Vehicle_condition'].max()
            col3.metric('Melhor Condição', melhor_cond)         
        
        with col4:
            pior_cond = df1.loc[:, 'Vehicle_condition'].min()
            col4.metric('Pior Condição', pior_cond)

    with st.container():
        st.markdown("""___""")
        st.title('Avaliações')

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### Avaliação média por Entregador")
            df1['Delivery_person_Ratings'] = pd.to_numeric(df1['Delivery_person_Ratings'], errors='coerce')
            df1 = df1.dropna(subset=['Delivery_person_Ratings'])
            df_avl_ratings = df1.loc[:, ['Delivery_person_ID', 'Delivery_person_Ratings']].groupby('Delivery_person_ID').mean().reset_index()
            st.dataframe(df_avl_ratings)

        with col2:
            st.markdown("##### Avaliação média por Trânsito")
            df_avg_rating_by_traffic = df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']].groupby('Road_traffic_density').agg({'Delivery_person_Ratings': ['mean', 'std']})
            df_avg_rating_by_traffic.columns = ['delivery_mean', 'delivery_std']
            df_avg_rating_by_traffic = df_avg_rating_by_traffic.reset_index()
            st.dataframe(df_avg_rating_by_traffic)
            
            st.markdown("##### Avaliação média por Clima")
            df_avg_rating_by_weather = df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']].groupby('Weatherconditions').agg({'Delivery_person_Ratings': ['mean', 'std']})
            df_avg_rating_by_weather.columns = ['delivery_mean', 'delivery_std']
            df_avg_rating_by_weather = df_avg_rating_by_weather.reset_index()
            st.dataframe(df_avg_rating_by_weather)

    with st.container():
        st.markdown("""___""")
        st.title('Velocidade da Entrega')

        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Top entregadores mais rápidos')
            df2 = (df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken_min']]
                      .groupby(['City', 'Delivery_person_ID'])
                      .mean()
                      .sort_values(['City', 'Time_taken_min'], ascending=True)
                      .reset_index())

            df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10) 
            df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10) 
            df_aux03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)

            df3 = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop=True)
            st.dataframe(df3)

        with col2:
            st.subheader('Top entregadores mais lentos')
            df2 = (df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken_min']]
                      .groupby(['City', 'Delivery_person_ID'])
                      .mean()
                      .sort_values(['City', 'Time_taken_min'], ascending=False)
                      .reset_index())

            df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10) 
            df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10) 
            df_aux03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)

            df3 = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop=True)
            st.dataframe(df3)

