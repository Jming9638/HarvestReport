import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from plotly import graph_objects as go


def count_weekdays(start_date, end_date):
    if start_date > end_date:
        start_date, end_date = end_date, start_date
    
    weekday_count = 0
    current_date = start_date
    
    while current_date <= end_date:
        if current_date.weekday() < 5:
            weekday_count += 1
        current_date += timedelta(days=1)
    
    return weekday_count


class HarvestReport:
    YES_NO_COLORMAP = {"Yes": "#0A9396", "No": "#BB3E03", "Leave": "#6C757D"}
    CONFIG = {"displayModeBar": False}
    
    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()
        self.data["Billable?"] = self.data.apply(lambda x: "Leave" if "Holiday" in x["Task"] else x["Billable?"], axis=1)

    def overall(self):
        billable_hours = self.data.groupby(["Billable?"]).agg({"Hours": "sum"}).reset_index()

        colors = [self.YES_NO_COLORMAP[billable] for billable in billable_hours["Billable?"]]

        fig = go.Figure()
        fig.add_trace(
            go.Pie(
                labels=billable_hours["Billable?"],
                values=billable_hours["Hours"],
                hole=0.3,
                text=billable_hours["Hours"],
                textfont=dict(size=16),
                texttemplate="%{percent:.2%}",
                hovertemplate="%{label}: %{value} hours <extra></extra>",
                marker=dict(colors=colors)
            )
        )

        fig.update_layout(
            title_text="Billable Hours",
            height=500,
            hoverlabel=dict(font_size=16)
        )

        st.plotly_chart(fig, use_container_width=True, config=self.CONFIG)
        
    def client_breakdown(self):
        exclude_client = [
            "Data - Internal",
            "Internal",
            "Persuasion",
            "PT Internal",
        ]
        cleaned_data = self.data[~self.data["Client"].isin(exclude_client)]
        client_hours = cleaned_data.groupby("Client").apply(
            lambda x: pd.Series({
                "billableHours": x[x["Billable?"] == "Yes"]["Hours"].sum(),
                "nonBillableHours": x[x["Billable?"] == "No"]["Hours"].sum(),
                "totalHours": x["Hours"].sum()
            })
        ).reset_index().sort_values("totalHours", ascending=False)

        fig = go.Figure()

        fig.add_traces(
            [
                go.Bar(
                    name="Billable Hours",
                    x=client_hours["Client"],
                    y=client_hours["billableHours"],
                    text=client_hours["billableHours"],
                    textfont=dict(size=16),
                    texttemplate="%{text:.2f}",
                    hovertemplate="%{x}: %{y} hours <extra></extra>",
                    marker_color="#0A9396"
                ),
                go.Bar(
                    name="Non-Billable Hours",
                    x=client_hours["Client"],
                    y=client_hours["nonBillableHours"],
                    text=client_hours["nonBillableHours"],
                    textfont=dict(size=16),
                    texttemplate="%{text:.2f}",
                    hovertemplate="%{x}: %{y} hours <extra></extra>",
                    marker_color="#BB3E03"
                )
            ]
        )

        fig.update_layout(
            barmode="stack",
            title="Client Breakdown",
            xaxis_title="Client",
            yaxis_title="Hours",
            height=500
        )

        st.plotly_chart(fig, use_container_width=True, config=self.CONFIG)
        
    def member_breakdown(self):
        member_hours = self.data.groupby("First Name").apply(
            lambda x: pd.Series({
                "billableHours": x[x["Billable?"] == "Yes"]["Hours"].sum(),
                "nonBillableHours": x[x["Billable?"] == "No"]["Hours"].sum(),
                "leaveHours": x[x["Billable?"] == "Leave"]["Hours"].sum(),
                "billablePercentage": x[x["Billable?"] == "Yes"]["Hours"].sum() / x["Hours"].sum(),
                "nonBillablePercentage": x[x["Billable?"] == "No"]["Hours"].sum() / x["Hours"].sum(),
                "totalHours": x["Hours"].sum()
            })
        ).reset_index().sort_values("First Name", ascending=True)
        
        fig = go.Figure()
        
        fig.add_traces(
            [
                go.Bar(
                    name="Billable Hours",
                    x=member_hours["First Name"],
                    y=member_hours["billableHours"],
                    text=member_hours["billableHours"],
                    textfont=dict(size=16),
                    texttemplate="%{text:.2f}",
                    hovertemplate="%{x}: %{y} hours <extra></extra>",
                    marker_color="#0A9396"
                ),
                go.Bar(
                    name="Non-Billable Hours",
                    x=member_hours["First Name"],
                    y=member_hours["nonBillableHours"],
                    text=member_hours["nonBillableHours"],
                    textfont=dict(size=16),
                    texttemplate="%{text:.2f}",
                    hovertemplate="%{x}: %{y} hours <extra></extra>",
                    marker_color="#BB3E03"
                ),
                go.Bar(
                    name="Leave",
                    x=member_hours["First Name"],
                    y=member_hours["leaveHours"],
                    text=member_hours["leaveHours"],
                    textfont=dict(size=16),
                    texttemplate="%{text:.2f}",
                    hovertemplate="%{x}: %{y} hours <extra></extra>",
                    marker_color="#6C757D"
                )
            ]
        )
        
        min_date = pd.to_datetime(self.data["Date"].min())
        max_date = pd.to_datetime(self.data["Date"].max())
        weekdays = count_weekdays(min_date, max_date)
        upper_bound = weekdays * 7
        lower_bound = upper_bound * 0.8
        
        fig.add_shape(
            type="line",
            x0=0 - 0.5,
            y0=upper_bound,
            x1=len(member_hours) + 0.5,
            y1=upper_bound,
            line=dict(
                color="#BB3E03",
                width=2,
                dash="longdash"
            )
        )
        # fig.add_annotation(
        #     x = len(member_hours) + 0.5,
        #     y = upper_bound,
        #     text="Critical",
        #     showarrow=False,
        #     xshift=-10,
        #     yshift=10,
        #     font=dict(
        #         size=16,
        #         color="black"
        #     )
        # )
        
        fig.add_shape(
            type="line",
            x0=0 - 0.5,
            y0=lower_bound,
            x1=len(member_hours) + 0.5,
            y1=lower_bound,
            line=dict(
                color="#0A9396",
                width=2,
                dash="longdash"
            )
        )
        # fig.add_annotation(
        #     x = len(member_hours) + 0.5,
        #     y = lower_bound,
        #     text="Enough",
        #     showarrow=False,
        #     xshift=-10,
        #     yshift=10,
        #     font=dict(
        #         size=16,
        #         color="black"
        #     )
        # )

        fig.update_layout(
            barmode="stack",
            title="Member Breakdown",
            xaxis_title="Member",
            yaxis_title="Hours",
            height=500
        )

        st.plotly_chart(fig, use_container_width=True, config=self.CONFIG)

    def task_detail(self):
        task_hours = self.data.groupby(["Client", "Task", "Billable?"]).agg({"Hours": "sum"}).reset_index()
        task_hours = task_hours.sort_values(["Billable?", "Hours"], ascending=[False, False])
        
        st.dataframe(
            data=task_hours,
            use_container_width=True,
            hide_index=True
        )

    def member_detail(self):
        member_pivot = self.data.pivot_table(
            index="First Name",
            columns="Date",
            values="Hours",
            aggfunc="sum",
            fill_value=0
        )
        
        st.dataframe(
            data=member_pivot,
            use_container_width=True,
            hide_index=False
        )
        