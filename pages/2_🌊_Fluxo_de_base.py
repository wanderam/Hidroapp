import pandas as pd
import streamlit as st
# import datetime as dt
# from datetime import datetime, timedelta
import plotly.express as px
# import plotly.graph_objects as go


#Configurando a página do app streamlit
st.set_page_config(
    page_title='Fluxo base',
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


# jndmirim = pd.read_csv(r'C:\Users\swat\Documents\app_vazao\pages\output_obs_jndmirim.csv')
# capivari = pd.read_csv(r'C:\Users\swat\Documents\app_vazao\pages\output_obs_capivari.csv')
# corumbatai = pd.read_csv(r'C:\Users\swat\Documents\app_vazao\pages\output_obs_corumbatai.csv')

# jndmirim['Date'] = pd.to_datetime(jndmirim['Date'])
# capivari['Date'] = pd.to_datetime(capivari['Date'])
# corumbatai['Date'] = pd.to_datetime(corumbatai['Date'])

################################################################

#Opções de escolha de bacias p/ o usuário
watersheds = df['Bacia'].unique().tolist()     # ['Jundiaí-Mirim', 'Capivari', 'Corumbatai']   ['Capivari', 'Corumbatai', 'Jundiaí-Mirim']

#Criando a sidebar
sidebar = st.sidebar.empty()

################################################################
#Mapas
mapa_jndmirim = 'pages/map_jndmirim.jpg'
mapa_capivari = 'pages/map_capivari.jpg'
mapa_corumbatai = 'pages/map_corumbatai.jpg'

#Areas das bacias
area_jndmirim = 95.45
area_capivari = 1276.88
area_corumbatai = 1718.47

################################################################

#Selectbox de seleção da bacia
st.sidebar.header('Escolha uma bacia')
watershed_select = st.sidebar.selectbox('Selecione', watersheds)

#Filtro de bacia
df2 = df.loc[df['Bacia'] == watershed_select, :]

#Convertendo a coluna de datas para o tipo datetime64
df2['Date'] = pd.to_datetime(df2['Date'])


# if watershed_select == 'Jundiaí-Mirim':
#     df = jndmirim
# elif watershed_select == 'Capivari':
#     df = capivari
# else:
#     df = corumbatai




#Definindo as datas mínimas e máximas de cada df
start_date = df2['Date'].min()    # datetime.today() - timedelta(days=5930) --> Outra forma de inserir datas       Data específica --> pd.to_datetime('2008-01-01')
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

#st.title(f'Daily streamflow and baseflow time series - Watershed: {watershed_select}')
st.header(f'Bacia: {watershed_select} | Período de dados: **{from_date.strftime('%d/%b/%Y')}** a **{to_date.strftime('%d/%b/%Y')}**')

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

    st.metric('Fluxo de base max. (m$^{3}$/s):', value=max_baseflow)
    st.metric('Fluxo de base mín. (m$^{3}$/s):', value=min_baseflow)
    st.metric('Fluxo de base médio (m$^{3}$/s):', value=mean_baseflow)

with col3:
    #area_bacia = df3.loc[0, 'Area'] --> tentar mostrar a área da bacia dessa forma. Porém, está dando erro no código

    if watershed_select == 'Jundiaí-Mirim':
        area_bacia = area_jndmirim
    elif watershed_select == 'Capivari':
        area_bacia = area_capivari
    else:
        area_bacia = area_corumbatai

    st.metric('Área (km$^{2}$)', value=area_bacia)

    #Indicando o período, em anos, disponível de dados para a bacia selecionada
    start_date = df2['Date'].min()
    end_date = df2['Date'].max()
    diff = (end_date.year - start_date.year) + 1
    st.metric('Período de dados (anos)', value=diff)

with col4:
    #Filtro do mapa da bacia selecionada
    if watershed_select == 'Jundiaí-Mirim':
        map = mapa_jndmirim
    elif watershed_select == 'Capivari':
        map = mapa_capivari
    else:
        map = mapa_corumbatai

    st.image(map, width=400)


# st.dataframe(df3)
st.divider()

col5, col6 = st.columns([0.8, 0.2])

with col5:
    #st.subheader('Series hydrograph')
    #st.markdown(f'Selected data from: **{from_date.strftime('%d/%b/%Y')}** to **{to_date.strftime('%d/%b/%Y')}**')
    graf_plotly = fig = px.line(df3, x='Date', y=['streamflow', 'baseflow'], color_discrete_sequence=['deepskyblue', 'indianred'],
                            labels={'Date': 'Date', 'streamflow': 'Streamflow', 'baseflow': 'B'},    #Não está dando certo aqui
                            markers=False,
                            height=400,
                            width=800)
    fig.update_traces(line_width=1)
    fig.update_yaxes(title_text='<b>Fluxo (m<sup>3</sup> s<sup>-1</sup>)</b>', title_font={"size": 14}, range=[0, None])
    fig.update_xaxes(title_text='<b>Tempo</b>', title_font={"size": 14})
    fig.update_layout(template='plotly', legend_title='<b>Legenda</b>')    # plotly_dark    simple_white
    fig.update_layout(legend=dict(font=dict(family='arial', size=14, color='dimgray')),
                    legend_title = dict(font=dict(family='arial', size=16, color='dimgray')))    # Century Gothic
    fig.add_hline(y=df2['streamflow'].mean(), line_color='red', line_width=1, line_dash='dash')

    #Para alterar os nomes das variáveis
    newlabels = {'streamflow': 'Vazão', 'baseflow': 'Fluxo base'}
    fig.for_each_trace(lambda t: t.update(name = newlabels[t.name],
                                          legendgroup = newlabels[t.name],
                                          hovertemplate = t.hovertemplate.replace(t.name, newlabels[t.name])
                                          )
                  )

    st.plotly_chart(graf_plotly, use_container_width=True)


#Dataframe dos dados
with col6:
    #st.subheader('Data table')
    #st.markdown(f'Selected data from: **{from_date.strftime('%d/%b/%Y')}** to **{to_date.strftime('%d/%b/%Y')}**')

    #@st.cache --> colocar essa linha de código no lugar certo para carregar os dados apenas uma vez
    def convert_df(df3):
        return df3.to_csv(index=False, float_format='%.2f', columns=['Date', 'streamflow', 'baseflow']).encode('utf-8')

    csv = convert_df(df3)

    st.dataframe(df3, width=250, height=300, hide_index=True, column_order=('Date', 'streamflow', 'baseflow'), use_container_width=True,
                 column_config={'Date': st.column_config.DatetimeColumn('Data', format="DD/MMM/YYYY"),
                                'streamflow': st.column_config.NumberColumn('Vazão', help="Série vazão", format='%.1f'),
                                'baseflow': st.column_config.NumberColumn('Fluxo base', help="Série fluxo de base", format='%.1f')})
    
    st.download_button('Baixar csv', csv, f'{watershed_select}'+'_dataset'+'.csv', 'text/csv', key='browser-data')    # O rótulo do botão era: Download csv


# st.dataframe(df3)
