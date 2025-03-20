import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
# import branca

st.set_page_config(
    page_title='Info',
    layout='wide',
    initial_sidebar_state='expanded'
)

#Texto na sidebar de apresentação do app
markdown = """
Este aplicativo via web exibe os resultados de uma pesquisa desenvolvida no PPG-IAC.

"""

st.sidebar.title('Sobre')
st.sidebar.info(markdown)
logo = 'Logo_IAC_d400.jpg'
st.sidebar.image(logo, width=100)

###############################################################################

st.title('Informações')

st.markdown(
        """
        Este aplicativo foi desenvolvido para divulgar os resultados da tese intitulada
        "DESEMPENHO DO MODELO HIDROLÓGICO SWAT NAS BACIAS HIDROGRÁFICAS DOS RIOS PIRACICABA, CAPIVARI E JUNDIAÍ: UMA ANÁLISE DO FLUXO DE BASE E DA RECARGA DE AQUÍFERO"
        desenvolvida no Programa de Pós-Graduação do [Instituto Agronômico de Campinas (IAC)](https://www.iac.sp.gov.br/)\n

        :green-background[**Instruções:**:point_down:]

        * A página :ocean:**Fluxo de base** exibe as séries temporais de vazão e fluxo de base da bacia hidrográfica selecionada. As séries de fluxo de base foram
        estimadas a partir de dados observados de vazão. O procedimento para separação foi realizado por meio da biblioteca Python ***Hydrograph-py*** ([Terink W, 2019](https://app.readthedocs.org/projects/hydrograph-py/downloads/pdf/latest/)).
        * A página :earth_americas:**Recarga** exibe os mapas de recarga de aquífero para a bacia hidrográfica selecionada. Os dados de recarga foram estimados por meio
        do modelo hidrológico ***SWAT-MODFLOW*** ([Bailey et al. 2016](https://onlinelibrary.wiley.com/doi/full/10.1002/hyp.10933)).        
        * Utilize o mapa interativo :world_map: abaixo para localizar as **sub-bacias PCJ**, bem como visualizar sua hidrografia.

        """
    )

st.caption('Autores: Wander A. Martins, Letícia L. Martins e Jener Fernando Leite de Moraes')

# st.markdown('Página do [Instituto Agronômico de Campinas](%s)' % 'https://www.iac.sp.gov.br/')
# st.markdown('Página da [PG-IAC](%s)' % 'https://www.iac.sp.gov.br/areadoinstituto/posgraduacao/')
    
###############################################################################
st.divider()


st.header('Sub-bacias PCJ')

subs_pcj = gpd.read_file('subs_pcj.geojson')                # Camada original --> C:\Users\swat\Documents\app_vazao\subs_pcj.geojson
drenagem = gpd.read_file('rede_drenagem.geojson')           # Camada de drenagem também está simplificada


centro = [-22.700, -47.150]
min_lat, max_lat = -21.000, -25.000
min_lon, max_lon = -45.000, -50.000

m = folium.Map(location=centro, tiles=None, control_scale=True, zoom_start=9, min_zoom=7, scrollWheelZoom=True,
               dragging=True, zoom_control=True, max_bounds=True, min_lat=min_lat, max_lat=max_lat, min_lon=min_lon, max_lon=max_lon)

#m.add_child(folium.LatLngPopup())

#Adicionando Marcadores de círculo para visualizar os limites do mapa
# folium.CircleMarker([max_lat, min_lon], color='navy', tooltip="Lower Right Corner").add_to(m)
# folium.CircleMarker([min_lat, min_lon], color='navy', tooltip="Upper Right Corner").add_to(m)
# folium.CircleMarker([min_lat, max_lon], color='navy', tooltip="Upper Left Corner").add_to(m)
# folium.CircleMarker([max_lat, max_lon], color='navy', tooltip="Lower Left Corner").add_to(m)


#Tiles

# white_BG = folium.TileLayer(tiles=branca.utilities.image_to_url([[1,1], [1,1]]), attr='W', name='White mode', overlay=False, control=True).add_to(m)    # fundo branco
basemap_dark = folium.TileLayer('cartodbdark_matter', name = 'Basemap (escuro)', overlay=False, control=True, min_zoom=7).add_to(m)
basemap_light = folium.TileLayer('cartodbpositron', name='Basemap (claro)', overlay=False, control=True, min_zoom=7).add_to(m)

#Manter o basemap_light na frente
m.keep_in_front(basemap_light)


# Mapa das sub-bacias da PCJ
#Função de estilo
style_function = lambda x: {
                   'fillColor': '#e6e6e6',
                   'fillOpacity': 0.4,
                   'color': 'black',
                   'weight': 0.6
                   }

#Função de destaque
def highlight_function(feature):
    return {
          'fillColor': '#87d4af',
          'fillOpacity': 0.4,
          'color': '#87d4af',
          'weight': 2.0
           }


#Sub-bacias PCJ
folium.GeoJson(subs_pcj, name='Sub-bacias PCJ', control=True, show=True, zoom_on_click=False,
               tooltip = folium.GeoJsonTooltip(fields = ['SUBS'],
                                               aliases = ['SUB-BACIA:'],
                                               sticky = True,
                                               labels=True,
                                               style = """
                                               background-color: #F0EFEF;
                                               border: 2px solid black;
                                               border-radius: 3px;
                                               box-shadow: 3px;
                                               """),
               style_function=style_function,
               highlight_function=highlight_function
               ).add_to(m)


#Rede de drenagem
folium.GeoJson(drenagem, name='Drenagem', control=True, show=True, zoom_on_click=False,
               style_function = lambda x: {
                   'color': 'deepskyblue',
                   'weight': 1.5}
                   ).add_to(m)


#Adicionar painel de controle de camadas
folium.LayerControl(collapsed=False).add_to(m)


st_mapa = st_folium(m, width=1000, height=600, use_container_width=False, returned_objects=[])    # Ver sobre "returned_objects" em https://folium.streamlit.app/static_map


#CRS da camada
# crs = subs_pcj.crs
# st.write(crs)
