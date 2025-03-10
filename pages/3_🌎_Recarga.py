import streamlit as st
# import geopandas as gpd
# import folium
# from streamlit_folium import st_folium

#Configurando a página do app streamlit
st.set_page_config(
    page_title='Recarga',
    layout='wide',
    initial_sidebar_state='expanded'
)

markdown = """
Esta página exibe mapas de recarga de aquífero.
"""

st.sidebar.title('Sobre')
st.sidebar.info(markdown)
# logo = 'pages/Logo_IAC_d400.jpg'
# st.sidebar.image(logo, width=100)

###############################################################################

#Criando a sidebar
sidebar = st.sidebar.empty()

list_watersheds = ['Atibaia cabeceira', 'Camanducaia', 'Capivari', 'Corumbataí', 'Jundiaí']

#Selectbox de seleção da bacia
st.sidebar.header('Escolha uma bacia')
watershed_select = st.sidebar.selectbox('Selecione', list_watersheds)

#Mapas das bacias
mapa_rec_atibaia_cab = 'pages/mapas_recarga/rch_map_atibaia_cabeceira.png'
mapa_rec_camanducaia = 'pages/mapas_recarga/rch_map_camanducaia.png'
mapa_rec_capivari = 'pages/mapas_recarga/rch_map_capivari.png'
mapa_rec_corumbatai = 'pages/mapas_recarga/rch_map_corumbatai.png'
mapa_rec_jundiai = 'pages/mapas_recarga/rch_map_jundiai.png'

if watershed_select == 'Atibaia cabeceira':
    recharge_map = mapa_rec_atibaia_cab
elif watershed_select == 'Camanducaia':
    recharge_map = mapa_rec_camanducaia
elif watershed_select == 'Capivari':
    recharge_map = mapa_rec_capivari
elif watershed_select == 'Corumbataí':
    recharge_map = mapa_rec_corumbatai
else:
    recharge_map = mapa_rec_jundiai


st.header('Recarga de aquífero das sub-bacias PCJ')
st.markdown("""
            Mapas de recarga de aquífero em escala mensal das sub-bacias PCJ, considerando o de Janeiro de 1985 a Dezembro de 2020.
            
            """)

st.divider()

atibaia_cabeceira_area = 1136.7
camanducaia_area = 1040.1
capivari_area = 1276.9
corumbatai_area = 1704.2
jundiai_area = 1125.2

if watershed_select == 'Atibaia cabeceira':
    area_bacia = atibaia_cabeceira_area
elif watershed_select == 'Camanducaia':
    area_bacia = camanducaia_area
elif watershed_select == 'Capivari':
    area_bacia = capivari_area
elif watershed_select == 'Corumbataí':
    area_bacia = corumbatai_area
else:
    area_bacia = jundiai_area


st.subheader(f'Bacia: {watershed_select} | Área: {area_bacia} km$^{2}$')
st.image(recharge_map, width=700)


# st.divider()