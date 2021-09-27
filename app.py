import json
from urllib.request import urlopen

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import streamlit as st


@st.cache
def load_data():
    # Load the data
    collisions = pd.read_csv(
        "collisions.csv"
    )
    collisions["FIPS"] = "0" + collisions["FIPS"].astype(str)
    return collisions


def introduction():
    # Load the data
    collisions = load_data()

    # Write the title and the subheader
    st.title("🚗 Mitigating Fatal Collisions Using California Traffic Collisions Data Set")
    st.subheader(
        "This simple web app aims to provide insights regarding the California Traffic Collisions Data Set "
        "sourced from Kaggle."
    )

    # Write details of the web app
    st.markdown(
        """
        In this web app, we aim to answer the following questions: 
        
        1. Where and when do fatal collisions occur? 
        2. Using the data, can we predict the conditions which would result to injurious collisions? 
        3. How do we mitigate these collisions?
        """
    )

    # Add image
    st.image("collision_photo.jpg")
    st.caption(
        f"Source: Forbes (https://www.forbes.com/sites/carltonreid/2020/09/28/journalists-should-stress-agency-in-reporting-on-traffic-crashes-states-new-media-guidelines).")


def generate_choropleth_map(year):
    # Load the data
    collisions = load_data()

    # Apply group by county
    if year == "all":
        collisions = collisions.groupby(["county", "FIPS"])["killed_victims"].sum().reset_index()
    else:
        year = int(year)
        collisions = collisions[collisions["collision_year"] == year]
        collisions = collisions.groupby(["county", "FIPS"])["killed_victims"].sum().reset_index()

    # Generate the choropleth map
    with urlopen("https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json") as response:
        counties = json.load(response)

    fig = px.choropleth(
        collisions,
        geojson=counties,
        locations="FIPS",
        color="killed_victims",
        color_continuous_scale="YlOrRd",
        scope="usa",
        hover_data=["county", "FIPS", "killed_victims"],
        labels={
            'county': "county",
            'killed_victims': 'fatalities'
        },
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )

    # Show the choropleth map
    st.markdown("**Number of collision fatalities for each county in California**")
    st.plotly_chart(fig)


def generate_collisions_by_hour_bar_graph(year):
    # Load the data
    collisions = load_data()

    # Apply group by hour
    if year == "all":
        collisions = collisions.groupby(["collision_hour"])["killed_victims"].sum().reset_index()
    else:
        year = int(year)
        collisions = collisions[collisions["collision_year"] == year]
        collisions = collisions.groupby(["collision_hour"])["killed_victims"].sum().reset_index()

    # Preprocess the data
    collisions = collisions.sort_values(by=['collision_hour'], ascending=True)

    # Plot the data
    fig, ax = plt.subplots(figsize=(6, 3), dpi=200)
    ax.bar(
        collisions["collision_hour"],
        collisions["killed_victims"],
    )
    ax.set_ylabel("Number of killed victims")
    ax.set_xlabel("Hour")
    st.markdown(
        "**Number of fatalities per hour due to collisions**"
    )
    st.pyplot(fig)


def generate_collisions_by_day_of_week_bar_graph(year):
    # Load the data
    collisions = load_data()

    # Apply group by collision day
    if year == "all":
        collisions = collisions.groupby(["collision_day"])["killed_victims"].sum().reset_index()
    else:
        year = int(year)
        collisions = collisions[collisions["collision_year"] == year]
        collisions = collisions.groupby(["collision_day"])["killed_victims"].sum().reset_index()

    # Preprocess the data
    collisions = collisions.sort_values(by=['collision_day'], ascending=True)
    days = {0: 'Mon', 1: 'Tues', 2: 'Weds', 3: 'Thurs', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
    collisions['collision_day'] = collisions['collision_day'].apply(lambda x: days[x])

    # Plot the data
    fig, ax = plt.subplots(figsize=(6, 3), dpi=200)
    ax.bar(
        collisions["collision_day"],
        collisions["killed_victims"],
    )
    ax.set_ylabel("Number of killed victims")
    ax.set_xlabel("Day of week")
    st.markdown(
        "**Number of fatalities per day of week due to collisions**"
    )
    st.pyplot(fig)


def descriptive_analytics():
    # Write the title and the subheader
    st.title("🚗 Analyzing Fatal Collisions")
    st.subheader(
        "This section aims to provide insights regarding the geographical and temporal aspect of fatal collisions."
    )

    # Generate year_options
    year_options = ["all"]
    year_list = range(2001, 2022)
    for year in year_list:
        year_options.append(year)

    # Ask for user input
    year = st.selectbox(
        "Select year",
        year_options
    )

    # Generate choropleth map
    generate_choropleth_map(year)

    # Generate temporal bar graphs
    generate_collisions_by_hour_bar_graph(year)
    generate_collisions_by_day_of_week_bar_graph(year)


def predictive_analytics():
    # Write the title and the subheader
    st.title("🚗 Predicting Injured Victims")
    st.subheader(
        "This section aims to provide a model to predict the number of injurious collisions."
    )

    # Outline steps (use ppt here)

    # Show step-by-step of modelling and results


def conclusion():
    # Write the title and the subheader
    st.title("🚗 Conclusions and Recommendations")

    # Outline conclusions and recommendations (use ppt here)


list_of_pages = [
    "The Data",
    "Analyzing Fatal Collisions",
    "Predicting Injured Victims",
    "Conclusions and Recommendations"
]

st.sidebar.title(':scroll: Main Pages')
selection = st.sidebar.radio("Go to: ", list_of_pages)

if selection == "The Data":
    introduction()

elif selection == "Analyzing Fatal Collisions":
    descriptive_analytics()

elif selection == "Predicting Injured Victims":
    predictive_analytics()

elif selection == "Conclusions and Recommendations":
    conclusion()
