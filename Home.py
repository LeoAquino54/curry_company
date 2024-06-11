import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
    page_icon="⬆️"
)

#image_path = 'D:/COMUNIDADE DS/PYTHON INICIANTE/CICLO_5/imgs/abstracte-png.webp'
image = Image.open('abstracte-png.webp')
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""____""")

st.write("# Curry Company Growth Dashboard")

st.markdown(
    """
    O Dashboard de Crescimento da Curry Company foi criado para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
    
    Aqui você encontrará análises detalhadas sobre o desempenho dos entregadores, a satisfação dos clientes, 
    bem como insights sobre as preferências dos usuários e tendências de mercado.
    
    Fique à vontade para explorar e extrair informações valiosas para impulsionar o crescimento do seu negócio!
    """)