import holidays
import pandas as pd
import streamlit as st

selected_country = holidays.country_holidays(country="MY", subdiv="SGR", years=[year for year in range(2021, 2028)])


def is_holiday(input_date):
    return "Yes" if input_date.date() in selected_country else "No"


def is_weekend(input_date):
    return "Yes" if input_date.weekday() >= 5 else "No"


@st.cache_data
def generate_dates(min_date, max_date):
    date_range = pd.date_range(start=min_date, end=max_date, freq="D")
    date_df = pd.DataFrame({"Date": date_range})

    date_df["isHoliday"] = date_df["Date"].dt.date.map(lambda x: "Yes" if x in selected_country else "No")
    date_df["isWeekend"] = date_df["Date"].dt.weekday.map(lambda x: "Yes" if x >= 5 else "No")

    date_df["Date"] = date_df["Date"].dt.strftime("%Y-%m-%d")

    return date_df
