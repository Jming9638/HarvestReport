import pandas as pd


def standardize(name):
    keywords = {"internal", "persuasion"}
    if any(keyword in name.lower() for keyword in keywords):
        return "Internal"
    return name


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
        self.member_date = None

    def transform(self):
        self.data["Client"] = self.data["Client"].apply(standardize)

        self.total_members += self.data["First Name"].nunique()
        self.total_hours += round(self.data["Hours"].sum(), 2)
        self.total_billable += round(self.data[self.data["Billable?"] == "Yes"]["Hours"].sum(), 2)
        self.total_non_billable += round(self.data[self.data["Billable?"] == "No"]["Hours"].sum(), 2)

        self.billable_hours = self.data.groupby(["Billable?"]).agg({"Hours": "sum"}).reset_index()

        self.client_hours = self.data.groupby(["Client"]).agg({"Hours": "sum"}).reset_index()
        self.client_billable_hours = self.data.groupby(["Client", "Billable?"]).agg({"Hours": "sum"}).reset_index()

        self.member_hours = self.data.groupby(["First Name"]).agg(
            BillableHours=("Hours", lambda x: x[self.data["Billable?"] == "Yes"].sum()),
            NonBillableHours=("Hours", lambda x: x[self.data["Billable?"] == "No"].sum()),
            TotalHours=("Hours", "sum")
        ).reset_index()
        self.member_hours["DefaultCapacity"] = 35.0
        self.member_hours["BillPercentage"] = self.member_hours["BillableHours"] / self.member_hours["TotalHours"]
        self.member_hours["NonBillPercentage"] = self.member_hours["NonBillableHours"] / self.member_hours["TotalHours"]

        self.member_date = self.data.pivot_table(
            values="Hours",
            index="First Name",
            columns="Date",
            aggfunc="sum",
            fill_value=0
        )
