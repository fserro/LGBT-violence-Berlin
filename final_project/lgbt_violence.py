import streamlit as st
import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pydeck as pdk

# TODO change favicon
favicon = 'https://image.spreadshirtmedia.net/image-server/v1/compositions/T141A1PA3623PT17X61Y15D133977900FS3231/views/1,width=650,height=650,appearanceId=1,backgroundColor=ffffff/the-emblem-of-the-capital-in-rainbow-colors-as-a-symbol-of-tolerance-and-openness.jpg'
berlin_rainbow = "./images/berlin_rainbow.png"
photo = "./images/gay_memorial.jpeg"
st.set_page_config(page_title='Violence against LGBTQIA* in Berlin', page_icon = favicon, layout = 'wide', initial_sidebar_state = 'auto')
col_1, col_2 = st.beta_columns([8,2])
with col_1:
    st.title('Mapping Violence against LGBTQIA* People in Berlin')

st.subheader('From 2014 until... just a few days ago.')

with col_2:
    st.image(berlin_rainbow)

st.write(
    "This website maps reported cases of violence against the LGBTQIA* community in Berlin.\n"
    "That's Lesbian, Gay, Bisexual, Transgender, Queer, and Instersex, Asexual and all those whose sexuality and identity fall outside of the cis-heteronormative model.\n"
    "\n"
    "In recent years, some menbers of the community have been reporting a perceived increase in the amount and intensity of gender violence in Berlin's streets.\n"
    "The goal of this project is to gather available data on this topic and to display it in a nice, interactive interface so everyone can learn more about the "
    "challenges faced not only by the community but by society in general.\n"
    "\n"
    "While the idea is to gather data from different sources, this first version works wih only one : the [Berliner Register](https://berliner-register.de/) website, "
    "which has been *tracking right-wing extremist and discriminatory incidents in Berlin* since 2014.\n"
    "\n"
    "I initially scrapped their website with `Requests` for all registered incidents since 2014, when the Berliner Register started keeping record of incidents \n"
    "more sistematically, until last week.")
st.write('I then compilled up all the data in a `Pandas` dataframe with almost than 22.000 rows!')

with open('pickles/df_complete.pickle', 'rb') as f:
    df_complete = pickle.load(f)
df_complete_shape = df_complete.shape
st.write("df_complete.shape: ", df_complete_shape)

st.write(df_complete)

st.write(
    'These stories concern all kinds of public manifestations of hate and aggression in Berlin, not particularly against any apecific group. There\'s racism, \n'
    'antisemitism, islamofobia, xenophobia. You name it... It also includes all types of violence: from stickers and graffiti promoting hate speech, \n'
    'to harrassment and physical aggression.')

st.write(
    'To extract only the stories concerning the LGBTQIA* community, I used the power of `Regular Expressions`in what is probably the longest RegEx string you have \n'
    'ever seen:'
)
st.write('`heteronormativ|gay|lgbt|lgtb|lbgt|ltgb|lgbqt|schwul|schwuchtel|lsbt|transgender|transphob|transsex|transfrau|transperson|transmann|transfeind|homophob|\n'
'queer|gleichgeschlecht|homosexu|homofeindlich|sexuelle[rn]* [ovi]|[^a-zöäüß]gender|binär`')

st.write(
    'This reduced the datapoints to just over 1000 incidents. I took some time to understand the data by reading some of the stories. I decided it made sense to \n'
    'classify the data and I came up with the following system:')

col_1, col_2, col_3 = st.beta_columns([2,6,2])
with col_2:
    '''

    * Attack (against individuals):
        * physical (or physical + verbal)
        * verbal
    * Propaganda (against community):
        * stickers, graffiti, banners, etc.
        * speeches by individuals and politicians, incl. in the municipal assemblies (*Bezirksverordnetenversammlung*, or BVV)
        * public expressions (oral and written) in media and online
    * Vandalism:
        * graffiti, damaging of LGBTQIA* symbols, memorials, plaques...
    * Structural Discrimination:
        * in workplace or public/private institutions
    * Reported Status to Police:
        * yes or no

    '''

st.write(
    'Then I needed to find the locations for the stories. I used `SpaCy`, which has a standard NLP model of the German language that parses text and automatically \n'
    'finds all types of entities, including locations and organizations. I then used those entities to find fitting coordinates by crosschecking if they can be \n'
    'found with `GeoPy`in the district where the incident took indeed place.')

st.write(
    'The categorization of the stories is still underway...'
)



RED_ICON_URL = "https://upload.wikimedia.org/wikipedia/commons/9/9e/WX_circle_red.png"
ORANGE_ICON_URL = "https://upload.wikimedia.org/wikipedia/commons/8/8b/WX_circle_orange.png"
# GREEN_ICON_URL = "https://upload.wikimedia.org/wikipedia/commons/5/50/WX_circle_green.png"
PURPLE_ICON_URL = "https://upload.wikimedia.org/wikipedia/commons/3/3d/WX_circle_purple.png"
LIGHTBLUE_ICON_URL = "https://upload.wikimedia.org/wikipedia/commons/d/d4/WX_circle_lightblue.png"
DARKBLUE_ICON_URL = "https://upload.wikimedia.org/wikipedia/commons/c/c3/WX_circle_darkblue.png"
# YELLOW_ICON_URL = "https://upload.wikimedia.org/wikipedia/en/f/fb/Yellow_icon.svg"

physical_icon_data = {
    # Icon from Wikimedia, used the Creative Commons Attribution-Share Alike 3.0
    # Unported, 2.5 Generic, 2.0 Generic and 1.0 Generic licenses
    "url": RED_ICON_URL,
    "width": 242,
    "height": 242,
    "anchorY": 242,
}
verbal_icon_data = {
    # Icon from Wikimedia, used the Creative Commons Attribution-Share Alike 3.0
    # Unported, 2.5 Generic, 2.0 Generic and 1.0 Generic licenses
    "url": ORANGE_ICON_URL,
    "width": 242,
    "height": 242,
    "anchorY": 242,
}

propaganda_icon_data = {
    # Icon from Wikimedia, used the Creative Commons Attribution-Share Alike 3.0
    # Unported, 2.5 Generic, 2.0 Generic and 1.0 Generic licenses
    "url": LIGHTBLUE_ICON_URL,
    "width": 242,
    "height": 242,
    "anchorY": 242,
}

vandalism_icon_data = {
    # Icon from Wikimedia, used the Creative Commons Attribution-Share Alike 3.0
    # Unported, 2.5 Generic, 2.0 Generic and 1.0 Generic licenses
    "url": DARKBLUE_ICON_URL,
    "width": 242,
    "height": 242,
    "anchorY": 242,
}

discrimination_icon_data = {
    # Icon from Wikimedia, used the Creative Commons Attribution-Share Alike 3.0
    # Unported, 2.5 Generic, 2.0 Generic and 1.0 Generic licenses
    "url": PURPLE_ICON_URL,
    "width": 242,
    "height": 242,
    "anchorY": 242,
}

def add_icon_info(df):
    df["icon_data"] = None
    for i in df[df['Attack'] == 'physical'].index:
        df["icon_data"][i] = physical_icon_data

    for i in df[df['Attack'] == 'verbal'].index:
        df["icon_data"][i] = verbal_icon_data

    for i in df[df['Propaganda'] == 'yes'].index:
        df["icon_data"][i] = propaganda_icon_data

    for i in df[df['Material Damage'] == 'yes'].index:
        df["icon_data"][i] = vandalism_icon_data

    for i in df[df['Structural Discrimination'] == 'yes'].index:
        df["icon_data"][i] = discrimination_icon_data
    return df


with open('pickles/df_map_test.pickle', 'rb') as f:
    df_map_DE = pickle.load(f)

df_map_DE = add_icon_info(df_map_DE)
df_map_DE['date_form'] = df_map_DE['Date'].apply(lambda d: d.strftime('%d %b %Y'))

with open('pickles/df_map_translated.pickle', 'rb') as f:
    df_map_EN= pickle.load(f)

df_map_EN = add_icon_info(df_map_EN)
df_map_EN['date_form'] = df_map_EN['Date'].apply(lambda d: d.strftime('%d %b %Y'))

df_map = df_map_DE




# view_state = pdk.data_utils.compute_view(df_map[["longitude", "latitude"]], 1)

# st.multiselect

st.write('Texts are by default in German but you can choose to read them in English too!')
col_1, col_2, col_3 = st.beta_columns([1,1, 18])
with col_1:
    if st.button('DE', key='de_map'):
        df_map = df_map_DE
with col_2:
    if st.button('EN', key='en_map'):
        df_map = df_map_EN

attacks = st.selectbox(
    'choose the type of incident',
    ['all incidents', 'physical attacks', 'verbal attacks', 'propaganda', 'vandalism', 'structural discrimination'])

if attacks == 'all incidents':
    df_map.dropna(inplace=True)
else:
    if attacks == 'physical attacks':
        df_map = df_map.loc[df_map['Attack'] == 'physical', df_map.columns]
    elif attacks == 'verbal attacks':
        df_map = df_map.loc[df_map['Attack'] == 'verbal', df_map.columns]
    elif attacks == 'propaganda':
        df_map = df_map.loc[df_map['Propaganda'] == 'yes', df_map.columns]
    elif attacks == 'vandalism':
        df_map = df_map.loc[df_map['Material Damage'] == 'yes', df_map.columns]
    elif attacks == 'structural discrimination':
        df_map = df_map.loc[df_map['Structural Discrimination'] == 'yes', df_map.columns]


col_1, col_2 = st.beta_columns([10,1])
with col_2:
    if st.button('ALL'):
        df_map = df_map[df_map['Date'].dt.year >= 2014]
    if st.button('2014'):
        df_map = df_map[df_map['Date'].dt.year == 2014]
    if st.button('2015'):
        df_map = df_map[df_map['Date'].dt.year == 2015]
    if st.button('2016'):
        df_map = df_map[df_map['Date'].dt.year == 2016]
    if st.button('2017'):
        df_map = df_map[df_map['Date'].dt.year == 2017]
    if st.button('2018'):
        df_map = df_map[df_map['Date'].dt.year == 2018]
    if st.button('2019'):
        df_map = df_map[df_map['Date'].dt.year == 2019]
    if st.button('2020'):
        df_map = df_map[df_map['Date'].dt.year == 2020]
    if st.button('2021'):
        df_map = df_map[df_map['Date'].dt.year == 2021]

st.write('Found', len(df_map), 'incidents')

# TODO: set fixed original view
view_state=pdk.ViewState(
    latitude=df_map['latitude'].iloc[0],
    longitude=df_map['longitude'].iloc[0],
    zoom=9.8,
    bearing=0,
    pitch=0
)


icon_layer = pdk.Layer(
    type="IconLayer",
    data=df_map,
    get_icon="icon_data",
    get_size=4,
    size_scale=15,
    get_position=["longitude", "latitude"],
    pickable=True,
)

tooltip={
    "html": "<b>Date:</b> {date_form}<br/><b>{Header}</b><br/> {Story} <br/> <b>Source:</b> {Source}",
    "style": {
        "backgroundColor": "grey",
        "color": "white", 
        "width": "500px"}
}
with col_1:
    st.pydeck_chart(pdk.Deck(map_style='mapbox://styles/mapbox/light-v9', layers=[icon_layer], initial_view_state=view_state, tooltip=tooltip))

with open('pickles/df_barplot_count.pickle', 'rb') as f:
    df_barplot_count= pickle.load(f)

st.subheader('Interactive Chart with Plotly')
fig = px.bar(
    df_barplot_count,
    x="District", y='count',
    color="type of incident",
    hover_name = 'type of incident',
    title="Incidents per District",
    range_y=[0,50],
    animation_frame="year",
    animation_group="District")

st.plotly_chart(fig, use_container_width=True)

with open('pickles/df_lgbt.pickle', 'rb') as f:
    df_lgbt_DE = pickle.load(f)

with open('pickles/df_lgbt_translated.pickle', 'rb') as f:
    df_lgbt_EN= pickle.load(f)

df_lgbt = df_lgbt_DE

st.write('This table contains all the incidents reported since 2014.')
"It's interactive! You can sort the columns by clicking on their title and hover over the stories to read them."
st.write('Choose a language:')
col_1, col_2, col_3 = st.beta_columns([1,1, 18])
with col_1:
    if st.button('DE', key='de_table'):
        df_lgbt = df_lgbt_DE
with col_2:
    if st.button('EN', key='en_table'):
        df_lgbt = df_lgbt_EN


df_lgbt[['date_form', 'District', 'Header', 'Story', 'Source', 'type of incident']]


st.subheader("What to do Next:")
'''
* Finish labeling the data
* Figuring out a way to desambiguate locations
* Adding an input form so visitors can report new cases
* Find data from other sources
* Train a NLP model with the labeled data to automaticlally detect if new incidents are relevant for this project
* Make a pipeline so new incidents data can be added automatically
'''

st.subheader("Tech Stack")

col_1, col_2, col_3, col_4, col_5 = st.beta_columns([2,2,2,2,2])
with col_1:
    st.image("tech stack/python-logo.png")
    st.image("tech stack/pandas.png")
    st.image("tech stack/Google_Translate_Icon.png")
with col_2:
    st.image("tech stack/bs.png")
    st.image("tech stack/logo-wide.png")
    st.image("tech stack/Requests-logo.png")

with col_3:
    st.image("tech stack/SpaCy_logo.svg.png")
    st.image("tech stack/numpy.png")
    st.image("tech stack/streamlit-logo-primary-colormark-darktext.png")

with col_4:
    st.image("tech stack/Plotly-logo-01-square.png")
    st.image("tech stack/RegEx-Logo-300x142.png")
    st.image("tech stack/jupyter.png")

with col_5:
    st.image("tech stack/pickle-rick.png")


