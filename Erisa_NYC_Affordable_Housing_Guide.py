"""
Name:       Erisa Bejgo
CS230:      Section  4
Data:       NY-House-Dataset
URL:        https://erisas-guide-to-affordable-living-in-nyc.streamlit.app

Description:
This program is for homeowners to look for an apartment/condo/house in NYC.
With different queries of what cities they want to be located in,
price ranges, square footage of the house, and
specific bedroom and bathrooms they are looking for, Erisa's
Real Estate website will help find all.There will be charts displaying
where residencies are the most and sliders to customize the
NYC Housing Market.

3 Idea Questions:
What location/city do you want to be stationed in?
What amount of bed/bathrooms are you looking for; per locality?
What real estate group do you identify with; give a key word?

Charts: Sliders (Price), Pie Chart (Localities/Bedroom/Bathroom), Bar Chart (House Type)
Click on Locality Buttons To Access Locations (Within Each)
Map: Including Every Destination

"""

import streamlit as st

st.set_page_config(page_title="Erisa's NYC Affordable House Guide")

#BACKGROUND COLOR
st.markdown("""
    <style>
        body {
            background-color: #f5f5dc;  /* Light beige */
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Cinquain&display=swap" rel="stylesheet">
    <h1 style='text-align: center; font-family: "Cinquain", serif; font-weight: bold; color: #8B008B; font-size: 48px; margin-bottom: 10px; letter-spacing: 3px;'>
        Erisa’s Guide to Affordable Living in NYC
    </h1>
""", unsafe_allow_html=True) #CHATGPT

st.markdown("""
    <h3 style='text-align: center; font-family: "Georgia", serif; color: #2F4F4F; margin-top: 5px;'>
        Explore Your NYC Housing Options!
    </h3>
""", unsafe_allow_html=True)

st.sidebar.success("Select a demo above.") #[ST4]

st.image("NYC.jpg", caption= "2025 New York", use_container_width =True)

st.markdown("""
    <style>
        .animated-image {
            width: 300px;
            animation: scale 5s infinite alternate;
        }

        @keyframes scale {
            from { transform: scale(1); }
            to { transform: scale(1.2); }
        }
        
        .caption {
            font-family: Georgia, serif;
            font-size: 16px;
            color: #444444;
            margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True) #CHATGPT

#IMPLEMENTING A TRANSITION
st.markdown("""
    <div style='text-align: center;'>
        <img src='https://images.pexels.com/photos/5825359/pexels-photo-5825359.jpeg?auto=compress&cs=tinysrgb&w=800' class='animated-image'>
    <p class='caption'></p>
    </div>
""", unsafe_allow_html=True)

st.markdown("<div class= 'spacer'></div>", unsafe_allow_html = True)

#3RD PICTURE
st.image("NYC (1).jpg", caption= "NYC Finds: New York County, Bronx County, Queens County, Richmond County, Kings County", use_container_width =True)

st.markdown("<div class= 'spacer'></div>", unsafe_allow_html = True)

st.markdown("""
    <style>
        .animated-image {
            width: 300px;
            animation: scale 5s infinite alternate;
        }

        @keyframes scale {
            from { transform: scale(1); }
            to { transform: scale(1.2); }
        }

        .caption {
            font-family: Georgia, serif;
            font-size: 16px;
            color: #444444;
            margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)  # CHATGPT

# IMPLEMENTING A TRANSITION
st.markdown("""
    <div style='text-align: center;'>
        <img src='https://images.pexels.com/photos/2260784/pexels-photo-2260784.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2' class='animated-image'>
    <p class='caption'></p>
    </div>
""", unsafe_allow_html=True)

st.markdown("<div class= 'spacer'></div>", unsafe_allow_html=True)

st.sidebar.title("Tourist Attractions in NYC")

st.sidebar.write("**New York:** Central Park, Times Square, Empire State")
st.sidebar.write("**Brooklyn:** Brooklyn Bridge, Coney Island, Dumbo")
st.sidebar.write("**Queens:** Flushing, Astoria, Gantry Plaza")
st.sidebar.write("**Bronx:** Bronx Zoo, Yankee Stadium, Botanical Garden")
st.sidebar.write("**Richmond:** Staten Island Ferry, Richmond Town, South Beach")

st.sidebar.write("Visit For More Information: https://www.tripadvisor.com/Attraction_Products-g60763-a_contentId.1178676632670054+268263072-New_York_City_New_York.html")
