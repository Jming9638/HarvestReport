import pandas as pd
from typing import Optional


class Transform:
    def __init__(self, data: pd.DataFrame):
        self.data = data

        self.total_members = 0
        self.total_hours = 0
        self.total_billable = 0
        self.total_non_billable = 0
        self.billable_hours = None
        self.client_hours = None
        self.client_billable_hours = None
        self.member_hours = None
        self.member_billable_hours = None
        self.members = None
        self.member_date = None

    def transform(self):
        self.total_members += self.data["First Name"].nunique()
        self.total_hours += round(self.data["Hours"].sum(), 2)
        self.total_billable += round(self.data[self.data["Billable?"] == "Yes"]["Hours"].sum(), 2)
        self.total_non_billable += round(self.data[self.data["Billable?"] == "No"]["Hours"].sum(), 2)

        self.billable_hours = self.data.groupby(["Billable?"]).agg({"Hours": "sum"}).reset_index()

        self.client_hours = self.data.groupby(["Client"]).agg({"Hours": "sum"}).reset_index()
        self.client_billable_hours = self.data.groupby(["Client", "Billable?"]).agg({"Hours": "sum"}).reset_index()

        self.member_hours = self.data.groupby(["First Name"]).agg(TotalHours=("Hours", "sum")).reset_index()
        self.member_billable_hours = self.data.groupby(["First Name", "Billable?"]).agg({"Hours": "sum"}).reset_index()

        self.members = self.member_billable_hours.merge(
            self.member_hours,
            left_on="First Name",
            right_on="First Name",
            how="left"
        )
        self.members["Percentage"] = self.members["Hours"] / self.members["TotalHours"]

        self.member_date = self.data.pivot_table(
            values="Hours",
            index="First Name",
            columns="Date",
            aggfunc="sum",
            fill_value=0
        )
        # self.member_date = self.member_date.map(lambda x: 1 if x > 0 else 0)
