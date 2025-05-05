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

#CLEAN LOCALITIES (removing New York, United States)
remove_localities = ['New York', 'United States']
df = df.drop(df[df['LOCALITY'].isin(remove_localities)].index) #drop:removes
df = df.reset_index(drop=True)
df,cleaned_column = clean_df_column(df)
df,cleaned_column = clean_df_column(df,'LOCALITY', 'The') #Cleans Column Again: removes "The Bronx" (two to one)
df['LOCALITY'] = df['LOCALITY'].str.strip() #gets rid of white spaces/prevents error in drop-down menu
df['LOCALITY'] = df['LOCALITY'].replace({'Flatbush': 'Kings', 'Brooklyn': 'Kings'})
#puts Flatbush, Brooklyn into Kings County as they reside there

#CLEAN TYPE, [DA7]
df, cleaned_column = clean_df_column(df, 'TYPE', "for sale")
df['TYPE'] = df['TYPE'].str.upper()
df['TYPE'] = df["TYPE"].dropna()

st.set_page_config(page_title="Real Estate Brokers of Your Localities")

#TITLE
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Cinquain&display=swap" rel="stylesheet">
    <h1 style='font-family: "Georgia", serif; font-weight: bold; color: #000000; font-size: 48px; margin-bottom: 10px; letter-spacing: 3px;'>
        Finding Brokers For Localities
    </h1>
""", unsafe_allow_html=True) #CHATGPT

st.sidebar.header("Finding A Broker In Your Locality")

#SELECTBOX, FILTER/REMOVES
st.subheader("What NYC County Are You Looking In?")
localities = df["LOCALITY"].dropna().unique()
selected_locality = st.selectbox("Select a Locality/County", sorted(localities))

filtered_data = df[df["LOCALITY"] == selected_locality]

#BROKERTITLE FOR EACH, FILTER/REMOVES AGAIN
if "BROKERTITLE" in filtered_data.columns:
    st.subheader(f"Brokers in {selected_locality}")

    #BROKERS & PROPERTIES
    broker_summary = (
        filtered_data.groupby("BROKERTITLE")["ADDRESS"]
        .nunique()
        .reset_index()
        .rename(columns={"ADDRESS": "Property Count"}) # PROPERTIES++
        .sort_values(by="Property Count", ascending=False)
    )

    #EXPAND/ARROW TO SEE BROKERS PROPERTIES (CHART), ITERATIONS
    for _, row in broker_summary.iterrows():
        broker = row["BROKERTITLE"]
        prop_count = row["Property Count"]

        with st.expander(f"{broker} — {prop_count} Properties"): #CHATGPT
            properties = (
                filtered_data[filtered_data["BROKERTITLE"] == broker]["ADDRESS"]
                .dropna()
                .unique()
            )
            for prop in properties:
                st.markdown(f"-{prop}")
else:
    st.warning("No Brokers In Locality!")

#SIDERBAR CUSTOMIZATION
st.sidebar.title("Find My Broker")

user_name = st.sidebar.text_input("What's your name?", placeholder="e.g. Erisa")

if user_name:
    st.sidebar.markdown(f"Hi **{user_name}**, let's find a broker for you!") #PRINT FOR USERS

    #DROPDOWN MENU/SELECTBOX, LOCALITY
    locality_options = df["LOCALITY"].dropna().unique()
    user_locality = st.sidebar.selectbox("Choose your locality:", sorted(locality_options))

    user_filtered = df[df["LOCALITY"] == user_locality]
    brokers = user_filtered["BROKERTITLE"].dropna().unique()

    #DROPDOWN MENU/SELECTBOX, BROKER
    if brokers.size > 0:
        selected_broker = st.sidebar.selectbox("Choose a broker:", sorted(brokers))

        #FINDS FILTERED ADDRESS
        broker_props = (
            user_filtered[user_filtered["BROKERTITLE"] == selected_broker]["ADDRESS"]
            .dropna()
            .unique()
        )

        #INFORMATION FOR USER INTERFACE
        st.sidebar.markdown(f"Properties by {selected_broker}")
        for prop in broker_props:
            st.sidebar.markdown(f"- {prop}")

        #CHECKBOX, THIS IS REALLY COOL IN MY CODE!
        contact = st.sidebar.checkbox("I want to be contacted by this broker!") #CHATGPT
        if contact:
            st.sidebar.success(f"Thanks {user_name}! We'll notify **{selected_broker}** to reach out to you soon.")
    else:
        st.sidebar.warning("No Brokers Found!")

