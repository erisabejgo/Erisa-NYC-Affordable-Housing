import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt
import seaborn as sns

def clean_df_column(df, column='LOCALITY', stringToRemove='County'):
    try:
        cleaned_column = [name.lower().replace(stringToRemove.lower(), '').title() for name in df[column]]
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
df['TYPE'] = df["TYPE"].dropna()

st.set_page_config(page_title="Real Estate Brokers of Your Localities")

st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Cinquain&display=swap" rel="stylesheet">
    <h1 style='font-family: "Georgia", serif; font-weight: bold; color: #000000; font-size: 48px; margin-bottom: 10px; letter-spacing: 3px;'>
        Finding Brokers For Localities
    </h1>
""", unsafe_allow_html=True) #CHATGPT

st.sidebar.header("Finding A Broker In Your Locality")

st.subheader("What NYC County Are You Looking In?")

localities = df["LOCALITY"].dropna().unique()  # Get unique localities
selected_locality = st.selectbox("Select a Locality/County", sorted(localities))
filtered_data = df[df["LOCALITY"] == selected_locality]

if "BROKERTITLE" in filtered_data.columns:
    st.subheader(f"Broker Titles in {selected_locality}")
    broker_titles = filtered_data["BROKERTITLE"].dropna().unique()
    st.write(broker_titles)
else:
    st.write("No Brokers In Locality!")