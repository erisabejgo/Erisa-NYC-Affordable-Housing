import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt
import seaborn as sns

#[DA1], [PY1], [PY2], [PY3], [PY4]
def clean_df_column(df, column='LOCALITY', stringToRemove='County'): #FOR ALL CODE
    try:
        cleaned_column = [name.lower().replace(stringToRemove.lower(), '').title() for name in df[column]] #lowercase, case sensitive for word "county"
        df[column] = cleaned_column
        return df, cleaned_column # 2 parameters returned df and cleaned_column
    except KeyError:
        print(f"Error: Column '{column}' not found in DataFrame.")
        return df, cleaned_column #prints out csv with cleaned_column and separate cleaned_column

df = pd.read_csv("NY-House-Dataset.csv") #FILE READ

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

#CLEAN BEDS, MAKES INT
df['BEDS'] = df['BEDS'].astype(int)

#CLEAN BATHS, MAKES INT
df['BATH'] = df['BATH'].astype(int)

st.set_page_config(page_title="Charts of Your Localities")

#TITLE OF PAGE
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Cinquain&display=swap" rel="stylesheet">
    <h1 style='font-family: "Georgia", serif; font-weight: bold; color: #000000; font-size: 48px; margin-bottom: 10px; letter-spacing: 3px;'>
        Understanding Locality/County Statistics
    </h1>
""", unsafe_allow_html=True) #CHATGPT

st.sidebar.header("Charts of Your Locality")

#DROPDOWN, [ST1]
st.subheader("Where do you want your home?")
localities = df["LOCALITY"].dropna().unique()  #Drops Unclean, Unique Values, Organized
selected_locality = st.selectbox("Select a Locality/County", sorted(localities))

#[DA1], FINDS JUST THAT LOCALITY DATA
filtered_data = df[df["LOCALITY"] == selected_locality]

# BEDROOMS PIE CHART [CHART1], MATPLOTLIB
st.subheader("Locality Houses Bedrooms")

bedroom_counts = filtered_data["BEDS"].value_counts()
fig1, ax1 = plt.subplots()

bedroom_colors = ['#F4C6C6', '#F5D0A9', '#A8E6A1', '#FFC3E1'] #CHATGPT

ax1.pie(bedroom_counts, labels=bedroom_counts.index, colors=bedroom_colors, autopct='%1.1f%%')
ax1.set_title(f"Bedrooms in {selected_locality}")
st.pyplot(fig1)

# BATHROOMS PIE CHART [CHART2], MATPLOTLIB
st.subheader("Locality Houses Bathrooms")

bathroom_colors = ['#F4C6C6', '#F5D0A9', '#A8E6A1', '#FFC3E1'] #CHATGPT

bathroom_counts = filtered_data["BATH"].value_counts()
fig2, ax2 = plt.subplots()
ax2.pie(bathroom_counts, labels=bathroom_counts.index, colors=bathroom_colors, autopct='%1.1f%%')
ax2.set_title(f"Bathrooms in {selected_locality}")
st.pyplot(fig2)

#TOP 20 UNITS (FILTERED), [DA2], [DA3]
st.subheader("TOP 20 UNITS WITH LOWEST PRICE PER SQ FOOTAGE")
filtered_data['PRICE_PER_SQFT'] = filtered_data['PRICE'] / filtered_data['PROPERTYSQFT']
filtered_data = filtered_data.sort_values(by='PRICE_PER_SQFT', ascending=True)
st.write(filtered_data[['LOCALITY','BROKERTITLE', 'TYPE', 'BEDS', 'BATH', 'ADDRESS', 'PRICE_PER_SQFT', 'PRICE']].head(20)) #20 FIRST IN DATA

#SEABORN1,[CHART3]
fig, ax = plt.subplots()
sns.countplot(data=filtered_data, x='TYPE',palette=['#006400']) #CHATGPT (COLORS)
plt.xticks(rotation=45)
ax.set_title("Number of Listings by Unit Type")
ax.set_xlabel("Type of Living Style", fontsize=14, color='black')
st.pyplot(fig)

#SIDEBAR
st.sidebar.title("Property Search Filters")
st.sidebar.write("Use Filters On This Page To Find Your Next Home!")

#USER INTERACTION + INFORMATION ON MIN AND MAX IN NYC (** BOLDS)
min_price_row = df.loc[df['PRICE'].idxmin()]
max_price_row = df.loc[df['PRICE'].idxmax()]

st.sidebar.title("Price Information")
st.sidebar.write(f"**Minimum Price**: ${min_price_row['PRICE']:,} in {min_price_row['LOCALITY']}")
st.sidebar.write(f"**Maximum Price**: ${max_price_row['PRICE']:,} in {max_price_row['LOCALITY']}")