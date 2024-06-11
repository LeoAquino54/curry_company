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
#arruma o tamanho dos gráficos
st.set_page_config(page_title='Visão Restaurantes', page_icon='📊', layout='wide')
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


def overall_metrics(df):
    """Esta função exibe as métricas gerais"""

    st.title("Overall Metrics")

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        delivery_unique = len(df['Delivery_person_ID'].unique())
        st.metric('Entregadores únicos', delivery_unique)

    with col2:
        cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
        df['distance'] = df[cols].apply(lambda x: haversine(
            (x['Restaurant_latitude'], x['Restaurant_longitude']),
            (x['Delivery_location_latitude'], x['Delivery_location_longitude'])
        ), axis=1)
        avg_distance = np.round(df['distance'].mean(), 2)
        st.metric('Distância média das entregas (km)', avg_distance)

    with col3:
        cols = ['Festival', 'Time_taken_min']
        df_aux = df.loc[:, cols].groupby('Festival').agg({'Time_taken_min': ['mean', 'std']})
        df_aux.columns = ['avg_time', 'std_time']
        df_aux = df_aux.reset_index()
        if not df_aux.empty and 'Yes' in df_aux['Festival'].values:
            avg_time_festival = np.round(df_aux.loc[df_aux['Festival'] == 'Yes', 'avg_time'].values[0], 2)
            st.metric('Tempo Médio de Entrega c/ Festival', avg_time_festival)
        else:
            st.warning("Não há dados disponíveis para o festival.")

    with col4:
        cols = ['Festival', 'Time_taken_min']
        df_aux = df.loc[:, cols].groupby('Festival').agg({'Time_taken_min': ['mean', 'std']})
        df_aux.columns = ['avg_time', 'std_time']
        df_aux = df_aux.reset_index()
        if not df_aux.empty and 'Yes' in df_aux['Festival'].values:
            avg_time_festival_std = np.round(df_aux.loc[df_aux['Festival'] == 'Yes', 'std_time'].values[0], 2)
            st.metric('STD c/ Festival', avg_time_festival_std)
        else:
            st.warning("Não há dados disponíveis para o festival.")
def delivery_city_distance(df):
    """Esta função exibe o tempo médio de entrega por cidade"""
    st.title("Tempo Médio de Entrega por Cidade")
    cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
    df['distance'] = df.loc[:, cols].apply(lambda x: haversine(
        (x['Restaurant_latitude'], x['Restaurant_longitude']),
        (x['Delivery_location_latitude'], x['Delivery_location_longitude'])
    ), axis=1)
    avg_distance = df.loc[:, ['City', 'distance']].groupby('City').mean().reset_index()
    fig = go.Figure(data=[go.Pie(labels=avg_distance['City'], values=avg_distance['distance'], pull=[0, 0.05, 0])])
    fig.update_layout(width=800, height=600)
    st.plotly_chart(fig)

def delivery_time_distribution(df):
    """Esta função exibe a distribuição do tempo de entrega"""
    st.title("Distribuição do Tempo")
    col1, col2 = st.columns([1, 1])
    with col1:
        df_aux = df.loc[:, ['City', 'Time_taken_min']].groupby(['City']).agg({'Time_taken_min': ['mean', 'std']})
        df_aux.columns = ['avg_time', 'std_time']
        df_aux = df_aux.reset_index()
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Control', x=df_aux['City'], y=df_aux['avg_time'], error_y=dict(type='data', array=df_aux['std_time'])))
        fig.update_layout(barmode='group')
        st.plotly_chart(fig)

    with col2:
        cols = ['City', 'Time_taken_min', 'Road_traffic_density']
        df_aux = df.loc[:, cols].groupby(['City', 'Road_traffic_density']).agg({'Time_taken_min': ['mean', 'std']})
        df_aux.columns = ['avg_time', 'std_time']
        df_aux.reset_index()
        df_aux.reset_index(inplace=True)  # Garanta que o DataFrame tenha um índice limpo
        fig = px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values='avg_time', color='std_time', color_continuous_scale='RdBu', color_continuous_midpoint=np.average(df_aux['std_time']))
        st.plotly_chart(fig)

def delivery_distance_distribution(df):
    """Esta função exibe a distribuição das distâncias"""
    st.title("Distribuição das Distâncias")
    cols = ['City', 'Time_taken_min' , 'Type_of_order']
    df_aux = df.loc[:, cols].groupby(['City', 'Type_of_order']).agg({'Time_taken_min': ['mean', 'std']})
    df_aux.columns = ['avg_time', 'std_time']
    df_aux.reset_index()
    st.dataframe(df_aux)


df = pd.read_csv('dataset/train.csv')
df = clean_code(df) 
df1 = df.copy()  

#================================================================================================
# Barra Lateral
#==========================================================================================
st.header("Marketplace - Visão Restaurantes")

image_path = 'D:/COMUNIDADE DS/PYTHON INICIANTE/CICLO_5/imgs/abstracte-png.webp'
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
date_slider_str = date_slider.strftime("%Y-%m-%d")  # Convertendo o valor do controle deslizante para uma string
df1['Order_Date'] = pd.to_datetime(df1['Order_Date'])  # Convertendo a coluna 'Order_Date' para datetime
linhas_selecionadas = df1['Order_Date'] < date_slider_str  # Comparando as datas convertidas
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de transito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

#================================================================================================
# Layout
#==========================================================================================

tab1,tab2,tab3 = st.tabs(['Visão Gerencial', '', ''])

with tab1:
    overall_metrics(df1)
    delivery_city_distance(df1)
    delivery_time_distribution(df1)
    delivery_distance_distribution(df1)



