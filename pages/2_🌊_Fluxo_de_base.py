import pandas as pd
import streamlit as st
# import datetime as dt
# from datetime import datetime, timedelta
import plotly.express as px
# import plotly.graph_objects as go
import geopandas as gpd
import matplotlib.pyplot as plt


#Configurando a página do app
st.set_page_config(
    page_title='Escoamento base',
    layout='wide',
    initial_sidebar_state='expanded'
)

###############################################################################

#Base de dados de vazão das bacias     --> Ver https://docs.streamlit.io/develop/concepts/architecture/caching
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

df = load_data('pages/all.csv')

################################################################

#Opções de escolha de bacias p/ o usuário
watersheds = df['Bacia'].unique().tolist()

#Criando a sidebar
sidebar = st.sidebar.empty()

################################################################
#Selectbox de seleção da bacia
st.sidebar.header('Escolha uma bacia')
watershed_select = st.sidebar.selectbox('Selecione', watersheds)

#Filtro de bacia
df2 = df.loc[df['Bacia'] == watershed_select, :]

#Convertendo a coluna de datas para o tipo datetime64
df2['Date'] = pd.to_datetime(df2['Date'])


#Definindo as datas mínimas e máximas de cada df
start_date = df2['Date'].min()
end_date = df2['Date'].max()


#Date input da data inicial e final
st.sidebar.header('Selecione um período')
from_date = st.sidebar.date_input('de:', value=start_date)

def show_success():
    st.toast('Intervalo aceito', icon="✅")

to_date = st.sidebar.date_input('a:', value=end_date, on_change=show_success, help='Aviso: escolha uma data maior que a data inicial')

if from_date > to_date:
    st.sidebar.error('Aviso: data inicial maior que a data final')
    df2 = df2

#Filtro de data para o df e gráfico
from_date = pd.to_datetime(from_date)
to_date = pd.to_datetime(to_date)
df3 = df2[df2['Date'].between(from_date, to_date)]

#Configurando o formato da data no df
data_formatada = df3['Date'].dt.strftime('%Y-%m-%d')    # %Y/%b/%d --> Sigla do mês    %Y-%m-%d --> Número do mês
df3['Date'] = data_formatada[0:]
###############################################################################
#Elementos da página principal

st.header('Escoamento de base das sub-bacias PCJ')

#Instruções sobre quebra de linhas em Markdown:
#Para quebrar uma linha sem adicionar espaço entre elas, adicione dois ou mais espaços ao final da primeira linha.
#Para quebrar uma linha adicionando espaço entre elas, adicionar "\n" ao final da primeira linha.
st.markdown("""
            Séries temporais diárias de vazão observada e escoamento de base estimado para as seguintes sub-bacias PCJ: **Atibaia Cabeceira**, **Camanducaia**, **Capivari**, **Corumbataí** e **Jundiaí**.  
                        
            :green-background[**Instruções:**:point_down:]

            * Utilize a caixa de seleção ao lado para selecionar a sub-bacia desejada.
            * Escolha uma data inicial e final no :calendar: ao lado para visualizar um período específico da série.
            * Visualize as séries no gráfico interativo :chart_with_upwards_trend: abaixo. Obs.: é possível baixar o gráfico no formato .png.
            * Ao final da página pode-se visualizar os dados em uma tabela interativa e baixá-los no formato .csv.
            * **Observação:** Neste estudo, especificamente para a bacia hidrográfica do rio Atibaia, foi considerada apenas a região de cabeceira, devido à localização do posto fluviométrico, com uma área de 1.136,7 km$^{2}$.

            """)

st.divider()


st.subheader(f'Bacia selecionada: :blue-background[{watershed_select}] | Período selecionado: :blue-background[{from_date.strftime('%d.%b.%Y')}] a :blue-background[{to_date.strftime('%d.%b.%Y')}]', divider='blue')
# st.markdown(':warning: Atenção: A área mostrada no mapa abaixo representa toda a bacia hidrográfica do rio Atibaia. A área da região de cabeceira considerada neste estudo é de 1.136,7 km$^{2}$')


col1, col2, col3, col4 = st.columns([0.2, 0.2, 0.2, 0.4])

with col1:
    max_streamflow = round(df3['streamflow'].max(), 2)
    min_streamflow = round(df3['streamflow'].min(), 2)
    mean_streamflow = round(df3['streamflow'].mean(), 2)
    
    st.metric('Vazão max. (m$^{3}$/s):', value=max_streamflow)
    st.metric('Vazão mín. (m$^{3}$/s):', value=min_streamflow)
    st.metric('Vazão média (m$^{3}$/s):', value=mean_streamflow)

with col2:
    max_baseflow = round(df3['baseflow'].max(), 2)
    min_baseflow = round(df3['baseflow'].min(), 2)
    mean_baseflow = round(df3['baseflow'].mean(), 2)

    st.metric('Esc. de base max. (m$^{3}$/s):', value=max_baseflow)
    st.metric('Esc. de base mín. (m$^{3}$/s):', value=min_baseflow)
    st.metric('Esc. de base médio (m$^{3}$/s):', value=mean_baseflow)


with col3:
    #Indicando o período, em anos, disponível de dados para a bacia selecionada
    start_date = df2['Date'].min()
    end_date = df2['Date'].max()
    diff = (end_date.year - start_date.year) + 1
    st.metric('Período de dados (anos)', value=diff)

    #Valor de BFI da bacia selecionada
    st.metric('BFI médio', value=0)   # --> substituir variável BFI aqui


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

with col4:
    st.pyplot(fig)


st.divider()


#Gráfico plotly das séries de vazão observada e escoamento de base
graf_plotly = fig = px.line(df3, x='Date', y=['streamflow', 'baseflow'], color_discrete_sequence=['deepskyblue', 'indianred'],
                            labels={'Date': 'Date', 'streamflow': 'Streamflow', 'baseflow': 'B'},  # verificar aqui
                            markers=False,
                            height=400,
                            width=800)

fig.update_traces(line_width=1)
fig.update_yaxes(title_text='<b>Vazão/Esc. de base (m<sup>3</sup> s<sup>-1</sup>)</b>', title_font={"size": 14}, range=[0, None])
fig.update_xaxes(title_text='<b>Tempo</b>', title_font={"size": 14})
fig.update_layout(template='plotly', legend_title='<b>Legenda</b>')    # plotly_dark    simple_white
fig.update_layout(legend=dict(font=dict(family='arial', size=14, color='dimgray')),
                    legend_title = dict(font=dict(family='arial', size=16, color='dimgray')))    # Century Gothic

fig.add_hline(y=mean_streamflow, line_color='red', line_width=1.0, line_dash='dash', opacity=0.7)

fig.update_layout(
    title_text=f'Vazão e escoamento de base da bacia hidrográfica do rio {watershed_select}',
    titlefont=dict(size=14, color='darkgray', family='Century Gothic')
    )

#Para alterar os nomes das variáveis
newlabels = {'streamflow': 'Vazão', 'baseflow': 'Esc. de base'}
fig.for_each_trace(lambda t: t.update(name = newlabels[t.name],
                                          legendgroup = newlabels[t.name],
                                          hovertemplate = t.hovertemplate.replace(t.name, newlabels[t.name])
                                          )
                  )

#Para exibir o gráfico plotly no app streamlit
st.plotly_chart(graf_plotly, use_container_width=True)


#Aviso gráfico plotly
st.caption(':warning: Obs.: A linha vermelha tracejada horizontal representa a vazão média do período selecionado.')
st.divider()

#Para exibir um df com os dados selecionados pelo usuário
st.dataframe(df3, width=300, height=400, hide_index=True, column_order=('Date', 'streamflow', 'baseflow'), use_container_width=False,
                 column_config={'Date': st.column_config.DatetimeColumn('Data', format="DD/MMM/YYYY"),
                                'streamflow': st.column_config.NumberColumn('Vazão', help="Série vazão", format='%.1f'),
                                'baseflow': st.column_config.NumberColumn('Esc. base', help="Série fluxo de base", format='%.1f')})

#Convertendo o df para .csv para ser baixado através do botão
def convert_df(df3):
    return df3.to_csv(index=False, float_format='%.2f', columns=['Date', 'streamflow', 'baseflow']).encode('utf-8')

csv = convert_df(df3)

#Exibir o botão para baixar o arquivo .csv
st.download_button('Baixar csv', csv, f'{watershed_select}'+'_dataset'+'.csv', 'text/csv', key='browser-data')    # O rótulo do botão era: Download csv
