import holidays
import pandas as pd

selected_country = holidays.country_holidays(
    country="MY",
    subdiv="SGR",
    years=[year for year in range(2022, 2030)]
)


def date_check(min_date, max_date):
    date_list = pd.date_range(start=min_date, end=max_date, freq="D")
    date_df = pd.DataFrame({"Date": date_list})
    
    date_df["isHoliday"] = date_df["Date"].dt.date.map(lambda x: "Yes" if x in selected_country else "No")
    date_df["isWeekend"] = date_df["Date"].dt.date.map(lambda x: "Yes" if x.weekday() in [5, 6] else "No")
    
    date_df["Date"] = date_df["Date"].dt.strftime("%Y-%m-%d")
    
    return date_df
