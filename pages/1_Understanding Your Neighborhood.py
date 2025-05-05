import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt
import seaborn as sns

#DA1, PY1, PY2, PY3, PY4
def clean_df_column(df, column='LOCALITY', stringToRemove='County'):
    try:
        cleaned_column = [name.lower().replace(stringToRemove.lower(), '').title() for name in df[column]]
        df[column] = cleaned_column
        return df, cleaned_column
    except KeyError:
        print(f"Error: Column '{column}' not found in DataFrame.")
        return df, cleaned_column

df = pd.read_csv("NY-House-Dataset.csv") #FILE READ

#CLEAN LOCALITIES
remove_localities = ['New York', 'United States']
df = df.drop(df[df['LOCALITY'].isin(remove_localities)].index)
df = df.reset_index(drop=True)
df,cleaned_column = clean_df_column(df)
df, cleaned_column = clean_df_column(df,'LOCALITY', 'The')
df['LOCALITY'] = df['LOCALITY'].str.strip()
df['LOCALITY'] = df['LOCALITY'].replace({'Flatbush': 'Kings', 'Brooklyn': 'Kings'})

#CLEAN TYPE, DA7
df, cleaned_column = clean_df_column(df, 'TYPE', "for sale")
df['TYPE'] = df['TYPE'].str.upper()
df['TYPE'] = df["TYPE"].dropna()

#CLEAN BEDS
df['BEDS'] = df['BEDS'].astype(int)

#CLEAN BATHS
df['BATH'] = df['BATH'].astype(int)

st.set_page_config(page_title="Charts of Your Localities")

st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Cinquain&display=swap" rel="stylesheet">
    <h1 style='font-family: "Georgia", serif; font-weight: bold; color: #000000; font-size: 48px; margin-bottom: 10px; letter-spacing: 3px;'>
        Understanding Locality/County Statistics
    </h1>
""", unsafe_allow_html=True) #ChatGPT

#st.markdown("# Understanding Locality/County Statistics")
st.sidebar.header("Charts of Your Locality")

#ST1
st.subheader("Where do you want your home?")
localities = df["LOCALITY"].dropna().unique()  # Get unique localities
selected_locality = st.selectbox("Select a Locality/County", sorted(localities))

#DA1
filtered_data = df[df["LOCALITY"] == selected_locality]

# BEDROOMS PIE CHART [CHART1] [CHART2]
st.subheader("Locality Houses Bedrooms")

bedroom_counts = filtered_data["BEDS"].value_counts()  # Count bedrooms
fig1, ax1 = plt.subplots()

bedroom_colors = ['#F4C6C6', '#F5D0A9', '#A8E6A1', '#FFC3E1'] #ChatGPT

ax1.pie(bedroom_counts, labels=bedroom_counts.index, colors=bedroom_colors, autopct='%1.1f%%')
ax1.set_title(f"Bedrooms in {selected_locality}")
st.pyplot(fig1)

# BATHROOMS PIE CHART
st.subheader("Locality Houses Bathrooms")

bathroom_colors = ['#F4C6C6', '#F5D0A9', '#A8E6A1', '#FFC3E1']

bathroom_counts = filtered_data["BATH"].value_counts()  # Count bathrooms
fig2, ax2 = plt.subplots()
ax2.pie(bathroom_counts, labels=bathroom_counts.index, colors=bathroom_colors, autopct='%1.1f%%')
ax2.set_title(f"Bathrooms in {selected_locality}")
st.pyplot(fig2)

#DA2, DA3
st.subheader("TOP 20 UNITS WITH LOWEST PRICE PER SQ FOOTAGE")
filtered_data['PRICE_PER_SQFT'] = filtered_data['PRICE'] / filtered_data['PROPERTYSQFT']
filtered_data = filtered_data.sort_values(by='PRICE_PER_SQFT', ascending=True)
st.write(filtered_data[['LOCALITY','BROKERTITLE', 'TYPE', 'BEDS', 'BATH', 'ADDRESS', 'PRICE_PER_SQFT', 'PRICE']].head(20))

#[SEABORN1][CHART3]
fig, ax = plt.subplots()
sns.countplot(data=filtered_data, x='TYPE',palette=['#006400'])
plt.xticks(rotation=45)
ax.set_title("Number of Listings by Unit Type")
ax.set_xlabel("Type of Living Style", fontsize=14, color='black')
st.pyplot(fig)