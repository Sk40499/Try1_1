import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.title("HR Dashboard")

# File upload
uploaded_file = st.file_uploader("Upload JSON or Excel file", type=["json", "xlsx"])

if uploaded_file is not None:
    try:
        # Read file
        if uploaded_file.name.endswith(".json"):
            df = pd.read_json(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("File uploaded successfully ✅")
        
        import plotly.express as px

        status_count = df["CURRENT STATUS"].value_counts().reset_index()
        status_count.columns = ["Status", "Count"]

        fig_status = px.pie(
        status_count,
       names="Status",
       values="Count",
       title="Employee Status Distribution"
)

        st.plotly_chart(fig_status)
        # Show data
        st.subheader("Data Preview")
        st.dataframe(df)

        # Convert date columns
        df["VISA EXPIRY"] = pd.to_datetime(df["VISA EXPIRY"], errors='coerce')
        df["CICPA EXPIRY"] = pd.to_datetime(df["CICPA EXPIRY"], errors='coerce')

        today = pd.Timestamp.today()
        next_90_days = today + pd.Timedelta(days=90)

        # Visa expiring soon
        visa_expiring = df[df["VISA EXPIRY"] < next_90_days]

        st.subheader("Visa Expiring Soon")
        st.write(visa_expiring[["NAME", "VISA EXPIRY"]])

        # CICPA expiring soon
        cicpa_expiring = df[df["CICPA EXPIRY"] < next_90_days]

        st.subheader("CICPA Expiring Soon")
        st.write(cicpa_expiring[["NAME", "CICPA EXPIRY"]])

        # Active employees
        active = df[df["CURRENT STATUS"].str.contains("Active", na=False)]
        st.metric("Active Employees", len(active))

        # Inactive employees
        inactive = df[df["CURRENT STATUS"].str.contains("Inactive", na=False)]
        st.metric("Inactive Employees", len(inactive))

    except Exception as e:
        st.error(f"Error: {e}")

else:
    st.warning("Please upload a file to view dashboard")