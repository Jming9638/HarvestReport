import pandas as pd
import streamlit as st
from datetime import datetime
from harvest.transform import Transform
from harvest.visual import Visual


def run():
    st.set_page_config(
        page_title="Harvest Report",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="auto"
    )

    st.title("Harvest Report")

    with st.sidebar:
        uploaded_file = st.file_uploader(
            label="Upload harvest csv report",
            type=["csv"],
            accept_multiple_files=False
        )

    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        min_date = data["Date"].min()
        max_date = data["Date"].max()

        with st.sidebar:
            st.markdown(f"Date range: **{min_date} - {max_date}**")

            client = st.selectbox(
                label="Client",
                options=[None] + sorted(data["Client"].unique().tolist())
            )

            employee = st.selectbox(
                label="Employee",
                options=[None] + sorted(data["First Name"].unique().tolist())
            )

        if client:
            data = data[data["Client"] == client]

        if employee:
            data = data[data["First Name"] == employee]

        transform = Transform(data)
        transform.transform()

        visual = Visual()

        visual_row1 = st.columns((2, 0.5, 1, 1), gap="small")
        with visual_row1[0]:
            visual.plotly_piechart(
                data=transform.billable_hours,
                title="Billable Hours",
                labels="Billable?",
                values="Hours"
            )
        with visual_row1[-2]:
            st.subheader("")
            st.metric(label="**Total Employee**", value=transform.total_members)
            st.metric(label="**Total Hour**", value=transform.total_hours)

        with visual_row1[-1]:
            st.subheader("")
            st.metric(label="**Total Billable Hour**", value=transform.total_billable)
            st.metric(label="**Total Non-billable Hour**", value=transform.total_non_billable)

        st.divider()

        client_hours = transform.client_hours.copy()
        client_hours["Hours"] = client_hours["Hours"].apply(lambda x: round(x, 2))
        client_hours = client_hours.sort_values(by=["Hours"], ascending=[False])
        visual.plotly_barchart(
            data=client_hours.head(10),
            title="Client Hours",
            labels="Client",
            values="Hours",
            orientation="v"
        )

        st.divider()

        visual.plotly_stackbar(
            data=transform.members,
            title="Employee Hours",
            labels="First Name",
            values="Percentage",
            orientation="v",
            barmode="stack",
            breakdown="Billable?"
        )

        st.divider()

        summary_table = transform.data.copy().groupby(["Client", "Task", "Billable?"]).agg({"Hours": "sum"}).reset_index()
        summary_table = summary_table.sort_values(
            by=["Billable?", "Hours"],
            ascending=[False, False]
        )
        st.dataframe(
            data=summary_table,
            hide_index=True,
            use_container_width=True
        )


if __name__ == "__main__":
    run()
