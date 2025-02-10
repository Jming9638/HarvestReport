import pandas as pd
import streamlit as st
from harvest.transform import Transform
from harvest.visual import Visual
from harvest.utils import generate_dates, is_holiday, is_weekend


def run():
    st.set_page_config(
        page_title="Harvest Report",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="auto"
    )

    st.title("Harvest Report")

    with st.sidebar:
        st.subheader("Upload harvest csv report")
        uploaded_file = st.file_uploader(
            label="Upload harvest csv report",
            type=["csv"],
            accept_multiple_files=False,
            label_visibility="collapsed"
        )

    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        min_date = data["Date"].min()
        max_date = data["Date"].max()

        report_date = generate_dates(min_date=min_date, max_date=max_date)

        with st.sidebar:
            st.divider()

            st.subheader(f"Date range: {min_date} - {max_date}")

            client = st.selectbox(
                label="**Client**",
                options=[None] + sorted(data["Client"].unique().tolist())
            )

            is_billable = st.selectbox(
                label="**Billable**",
                options=[None] + sorted(data["Billable?"].unique().tolist())
            )

            employee = st.selectbox(
                label="**Employee**",
                options=[None] + sorted(data["First Name"].unique().tolist())
            )

            st.divider()

            st.markdown("**Holiday and Weekend**")
            st.dataframe(
                data=report_date,
                hide_index=True,
                use_container_width=True
            )

        if client:
            data = data[data["Client"] == client]

        if is_billable:
            data = data[data["Billable?"] == is_billable]

        if employee:
            data = data[data["First Name"] == employee]

        transform = Transform(data)
        transform.transform()

        visual = Visual()

        visual_row1 = st.columns((2, 0.5, 1, 1), gap="small")
        with visual_row1[0]:
            colormap = {
                "Yes": "#0A9396",
                "No": "#BB3E03"
            }

            visual.plotly_piechart(
                data=transform.billable_hours,
                title="Billable Hours",
                labels="Billable?",
                values="Hours",
                colormap=colormap
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
        top_client = 15
        visual.plotly_barchart(
            data=client_hours.head(top_client),
            title=f"Client Hours (Top {top_client})",
            labels="Client",
            values="Hours",
            orientation="v"
        )

        st.divider()

        member_hours = transform.members.copy()
        member_hours = member_hours.sort_values(
            by=["First Name", "Billable?"],
            ascending=[True, False]
        )

        visual.plotly_stackbar(
            data=member_hours,
            title="Employee Hours",
            labels="First Name",
            values="Percentage",
            orientation="v",
            barmode="stack",
            breakdown="Billable?"
        )

        st.divider()

        st.markdown("**Detailed Table**")
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

        st.divider()
        with st.expander("**Detailed Hours**"):
            st.dataframe(
                data=transform.member_date,
                hide_index=False,
                use_container_width=True
            )


if __name__ == "__main__":
    run()
