import streamlit as st
import pandas as pd
import datetime
import altair as alt
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects

from config.config import Config as conf

st.title("!!!Where is Covid Now!!!")

DATE_COLUMN = "date_reported"


COUNTRY_NAME_DICT = {
    'United States of America': "USA",
    "United Kingdom": 'UK',
    "Russian Federation": 'Russia'

}

def to_lower_case(x):
    return str(x).lower()

def shorten_country_name(x):
    return

def fetch_load_data():
    # data = pd.read_csv(conf.load_configs().get("site").get("url"), nrows=1000)
    data = pd.read_csv("/Users/soonam/Downloads/WHO-COVID-19-global-data.csv")
    data.rename(to_lower_case, axis="columns", inplace=True)
    return data


data_loding_state = st.text("Loading the data.....")
data = fetch_load_data()
data_loding_state.text("")

yesterday = datetime.date.today() - datetime.timedelta(days=1)
date = st.date_input("Date", yesterday)
dt64 = np.datetime64(date)

filtered_data = data.loc[data[DATE_COLUMN] == str(dt64)]

def create_new_cases_deaths(filtered_data):
    return st.markdown(
        "**Total new cases:** {}  \n".format(filtered_data["new_cases"].sum())
        + "**Total new deaths:** {}".format(filtered_data["new_deaths"].sum())
    )


def create_top_ten_country_chart(filtered_data):
    st.subheader("Top 10 Countries by new cases")
    top_ten_data = filtered_data.sort_values(by="new_cases", ascending=False).iloc[:10]
    top_ten_data['country'] = top_ten_data['country'].apply(lambda x: COUNTRY_NAME_DICT.get(x, x))

    st.write(
        alt.Chart(top_ten_data, width=800, height=500)
        .mark_bar(color='firebrick')
        .encode(
            x=alt.X(
                "country", sort=None, title="Countries"
            ),
            y=alt.Y("new_cases", title="Number of New Cases")
        )
        .configure_axisX(titleAngle=0, labelAngle=0),
    )



def create_top_ten_country_line_chart(filtered_data):
    st.subheader("Top 10 Countries by new cases")

    from_date = datetime.date.today() - datetime.timedelta(days=365)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN], format='%Y-%m-%d')
    dt64 = np.datetime64(from_date)

    filtered_data = filtered_data.loc[data[DATE_COLUMN] >= str(dt64)]
    filtered_data['month'] = filtered_data[DATE_COLUMN].dt.month
    filtered_data['year'] = filtered_data[DATE_COLUMN].dt.year

    final_data = filtered_data.groupby(["month",'year'])['new_cases'].sum().reset_index()

    st.write(
        alt.Chart(final_data, width=800, height=500)
        .mark_line()
        .encode(
            x=alt.X(
                "month", sort=None, title="Year of the Month"
            ),
            y=alt.Y("new_cases", title="Number of New Cases"),
            color='new_cases',
        )
        .configure_axisX(titleAngle=0, labelAngle=0),
    )


def show_choropleth(filtered_data):
    final_data = filtered_data.drop(filtered_data[filtered_data["new_cases"] == 0].index)
    st.subheader("Global Map of Coronavirus Cases")
    fig = px.choropleth(final_data, locations="country_code",
                        color="cumulative_cases",
                        hover_name="country_code",
                        animation_frame="country_code",
                        title="", color_continuous_scale=px.colors.sequential.PuRd)

    fig


create_new_cases_deaths(filtered_data)
create_top_ten_country_chart(filtered_data)
show_choropleth(filtered_data)
create_top_ten_country_line_chart(data)
