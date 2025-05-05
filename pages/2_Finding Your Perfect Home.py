import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt
import seaborn as sns


def clean_df_column(df, column='LOCALITY', stringToRemove='County'):
    try:
        cleaned_column = [name.replace(stringToRemove, '').title() for name in df[column]]
        df[column] = cleaned_column
        return df, cleaned_column
    except KeyError:
        print(f"Error: Column '{column}' not found in DataFrame.")
        return df, cleaned_column

df = pd.read_csv("NY-House-Dataset.csv")


#CLEAN LOCALITIES
remove_localities = ['New York', 'United States']
df = df.drop(df[df['LOCALITY'].isin(remove_localities)].index)
df = df.reset_index(drop=True)
df,cleaned_column = clean_df_column(df)
df, cleaned_column = clean_df_column(df,'LOCALITY', 'The')
df['LOCALITY'] = df['LOCALITY'].str.strip()
df['LOCALITY'] = df['LOCALITY'].replace({'Flatbush': 'Kings', 'Brooklyn': 'Kings'})

#CLEAN TYPE
df, cleaned_column = clean_df_column(df, 'TYPE', "for sale")
df['TYPE'] = df['TYPE'].str.upper()

#CLEAN BEDS
df['BEDS'] = df['BEDS'].astype(int)

#CLEAN BATHS
df['BATH'] = df['BATH'].astype(int)


st.set_page_config(page_title="Location of NYC Homes")
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Cinquain&display=swap" rel="stylesheet">
    <h1 style='font-family: "Georgia", serif; font-weight: bold; color: #000000; font-size: 48px; margin-bottom: 10px; letter-spacing: 3px;'>
        Location of NYC Homes
    </h1>
""", unsafe_allow_html=True)

st.sidebar.header("Location of Your Localities")

#st.markdown("# Location of NYC Homes")

localities = df["LOCALITY"].dropna().unique()

#ST2
options = st.multiselect(
    "What NYC County Are You Connecting With?",
    localities
)

#ST3, DA5
max_price = int(df['PRICE'].max())
min_price = int(df['PRICE'].min())

price_range = st.slider("Choose Your Listing Price Range", min_price, max_price, (min_price, max_price))
st.write("NYC Price Range", price_range)

min_bedroom = int(df['BEDS'].min())
max_bedroom = int(df['BEDS'].max())

bed_range = st.slider("Choose How Many Bedrooms You Want", min_bedroom, max_bedroom,(min_bedroom, max_bedroom))
st.write("Bedroom Range", bed_range)

min_bathroom = int(df['BATH'].min())
max_bathroom = int(df['BATH'].max())

bath_range = st.slider("Choose How Many Bathrooms You Want", min_bathroom, max_bathroom, (min_bathroom, max_bathroom))
st.write("Bathroom Range", bath_range)

filtered_df = df[

    (df['LOCALITY'].isin(options)) &
    (df['PRICE'] >= price_range[0]) & (df['PRICE'] <= price_range[1]) &
    (df['BEDS'] >= bed_range[0]) & (df['BEDS'] <= bed_range[1]) &
    (df['BATH'] >= bath_range[0]) & (df['BATH'] <= bath_range[1])
]

#st.map(filtered_df, latitude= "LATITUDE", longitude= "LONGITUDE")

#DA4, DA9
filtered_df["size"] = filtered_df['PROPERTYSQFT']/ 10


#[ST4][MAP]
point_layer = pdk.Layer(
    "ScatterplotLayer",
    data=filtered_df,
    id="nyc-units",
    get_position=['LONGITUDE', 'LATITUDE'],
    get_color="[0, 100, 0]",
    pickable=True,
    auto_highlight=True,
    get_radius="size",
)

view_state = pdk.ViewState( #CHATGPT
    latitude=40.7128,
    longitude=-74.0060,
    controller=True,
    zoom=10.5,
    pitch=30
)

chart = pdk.Deck(
    point_layer,
    initial_view_state=view_state,
    map_style = "light",
    tooltip={"text": "{ADDRESS}, PRICE: $ {PRICE}"},
)

event = st.pydeck_chart(chart, on_select="rerun", selection_mode="multi-object")


