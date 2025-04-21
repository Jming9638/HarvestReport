import pandas as pd
import streamlit as st
from harvest.harvest import HarvestReport
from harvest.utils import date_check


def run():
    st.set_page_config(
        page_title="Harvest Report",
        page_icon="",
        layout="wide",
        initial_sidebar_state="auto",
    )

    st.title("Harvest Report")
    
    with st.sidebar:
        st.markdown("## Upload harvest report.")
        uploaded_file = st.file_uploader(
            label="Upload csv file",
            type=["csv"],
            accept_multiple_files=False,
            label_visibility="collapsed",
        )
        st.divider()
        
    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        min_date = data["Date"].min()
        max_date = data["Date"].max()
        
        with st.sidebar:
            st.subheader(f"Date: {min_date} - {max_date}")
            
            client = st.selectbox(
                label="**Client**",
                options=[None] + sorted(data["Client"].unique().tolist()),
            )
            
            billable = st.selectbox(
                label="**Billable?**",
                options=[None] + sorted(data["Billable?"].unique().tolist()),
            )
            
            employee = st.selectbox(
                label="**Employee**",
                options=[None] + sorted(data["First Name"].unique().tolist()),
            )
            st.divider()
            
            st.markdown("**Holday and Weekend**")
            date_properties = date_check(min_date, max_date)
            st.dataframe(
                data=date_properties,
                use_container_width=True,
                hide_index=True
            )
        
        if client:
            data = data[data["Client"] == client]
            
        if billable:
            data = data[data["Billable?"] == billable]
            
        if employee:
            data = data[data["First Name"] == employee]
            
        reporter = HarvestReport(data)
        
        visual_cols = st.columns((2, 0.5, 1, 1), gap="small", vertical_alignment="center")
        with visual_cols[0]:
            reporter.overall()
            
        with visual_cols[2]:
            st.metric(label="Total Employee", value=len(data["First Name"].unique()))
            st.metric(label="Total Billable Hours", value=round(data[data["Billable?"] == "Yes"]["Hours"].sum(), 2))
            
        with visual_cols[3]:
            st.metric(label="Total Hours", value=round(data["Hours"].sum(), 2))
            st.metric(label="Total Non-Billable Hours", value=round(data[data["Billable?"] == "No"]["Hours"].sum(), 2))
        
        st.divider()
        
        reporter.client_breakdown()
        st.divider()
        
        reporter.member_breakdown()
        st.divider()
        
        st.markdown("**Task Breakdown**")
        reporter.task_detail()
        st.divider()
        
        with st.expander("**Detailed Hours**"):
            reporter.member_detail()
    
    
if __name__ == "__main__":
    run()
