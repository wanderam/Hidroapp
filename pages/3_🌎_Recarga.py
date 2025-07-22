import streamlit as st
# import folium
# from streamlit_folium import st_folium
import geopandas as gpd
import matplotlib.pyplot as plt



#Configurando a página do app
st.set_page_config(
    page_title='Recarga',
    layout='wide',
    initial_sidebar_state='expanded'
)

###############################################################################

#Criando a sidebar
sidebar = st.sidebar.empty()

list_watersheds = ['Atibaia', 'Camanducaia', 'Capivari', 'Corumbataí', 'Jundiaí']

#Selectbox de seleção da bacia
st.sidebar.header('Escolha uma bacia')
watershed_select = st.sidebar.selectbox('Selecione', list_watersheds)

#Mapas das bacias
mapa_rec_atibaia_cab = 'pages/mapas_recarga/rch_map_atibaia_cabeceira.png'
mapa_rec_camanducaia = 'pages/mapas_recarga/rch_map_camanducaia.png'
mapa_rec_capivari = 'pages/mapas_recarga/rch_map_capivari.png'
mapa_rec_corumbatai = 'pages/mapas_recarga/rch_map_corumbatai.png'
mapa_rec_jundiai = 'pages/mapas_recarga/rch_map_jundiai.png'

if watershed_select == 'Atibaia':
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


#Sobre Markdown:
#Para quebrar uma linha sem adicionar espaço entre elas, adicione dois ou mais espaços ao final da primeira linha.
#Para quebrar uma linha adicionando espaço entre elas, adicionar "\n" ao final da primeira linha.
st.markdown("""
            Mapas de recarga de aquífero média mensal das seguintes sub-bacias PCJ: **Atibaia Cabeceira**, **Camanducaia**, **Capivari**, **Corumbataí** e **Jundiaí**.  
            O período de modelagem considerado foi de **Janeiro de 1985** a **Dezembro de 2020**.  
            Dimensões da célula da grade do modelo: 250 x 250 m | Área total da célula: 62.500 m$^{2}$.
            
            :green-background[**Instruções:**:point_down:]
            * Utilize a caixa de seleção ao lado para selecionar a sub-bacia desejada.
            * **Observação:** Neste estudo, especificamente para a bacia hidrográfica do rio Atibaia, foi considerada apenas a região de cabeceira, devido à localização do posto fluviométrico, com uma área de 1.136,7 km$^{2}$.

            """)


st.divider()

col1, col2 = st.columns([0.6, 0.4])

with col1:
    atibaia_cabeceira_area = 1136.7
    camanducaia_area = 1040.1
    capivari_area = 1276.9
    corumbatai_area = 1704.2
    jundiai_area = 1125.2

    if watershed_select == 'Atibaia':
        area_bacia = atibaia_cabeceira_area
    elif watershed_select == 'Camanducaia':
        area_bacia = camanducaia_area
    elif watershed_select == 'Capivari':
        area_bacia = capivari_area
    elif watershed_select == 'Corumbataí':
        area_bacia = corumbatai_area
    else:
        area_bacia = jundiai_area


    st.subheader(f'Bacia selecionada: :blue-background[{watershed_select}]')    #  | Área: :blue-background[{area_bacia} km$^{2}$]
    st.image(recharge_map, width=700)


#MAPA COM DESTAQUE DA SUB-BACIA SELECIONADA PELO USUÁRIO
#Lendo a camada de sub-bacias PCJ no formato .geojson
gdf = gpd.read_file('subs_pcj.geojson')

#Filtrando a sub-bacia selecionada pelo usuário
bacia_destacada = gdf.loc[gdf['SUBS'] == watershed_select]

bacia_destacada_utm = bacia_destacada.copy(deep=True)
bacia_destacada_utm.to_crs(epsg='32723', inplace=True)
bacia_destacada_utm['area_km2'] = bacia_destacada_utm['geometry'].area / 10**6
area_bacia_km2 = bacia_destacada_utm.iloc[0, -1]

#Criando uma figura do plt para plotar os dois mapas
fig, ax = plt.subplots(1, 1)

#Mapa das sub-bacias PCJ
gdf.plot(ax=ax, color='whitesmoke', edgecolor='darkgrey', lw=0.4, ls='-', zorder=1)

#Mapa da sub-bacia selecionada com destaque
bacia_destacada.plot(ax=ax, color='#87d4af', alpha=1.0, edgecolor='#01984f', lw=0.8, ls='-', zorder=2)

#Demais componentes do mapa
# ax.set_title(f'{watershed_select}', fontsize=16, color='k', weight='bold')
ax.text(0.6, 0.8, f'Área:\n{round(area_bacia_km2, 1)} km$^{2}$', transform=ax.transAxes, va='center', ha='center', color='k', fontsize=14, fontweight='ultralight', fontfamily='monospace', alpha=0.6)    # bbox=dict(facecolor='gray', alpha=0.5, edgecolor='k', ls='--', lw=0.8)
ax.set_axis_off()


with col2:
    st.pyplot(fig)

