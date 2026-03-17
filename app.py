import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="QA Metrics Dashboard", layout="wide")

# --- DATA PERSISTENCE ---
# We use a CSV to store data so multiple users see the same updates
DATA_FILE = "qa_data.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        # Default starting data based on your screenshots
        return pd.DataFrame({
            "Metric": ["Total Defects", "Critical Defects", "Defect Leakage %", "Test Execution %", "Automation Coverage %"],
            "Value": [0, 0, 0, 0, 0],
            "Target": ["-", "Decreasing", "<5%", "100%", "Increasing"]
        })

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# --- SIMPLE LOGIN SYSTEM ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("🔐 QA Dashboard Login")
    user = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if user == "admin" and password == "qa123": # Simple hardcoded creds
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("Invalid credentials")
    st.stop()

# --- MAIN APP ---
st.title("📊 QA Metrics Dashboard")

# Sidebar for Navigation and Uploads
with st.sidebar:
    st.header("Controls")
    mode = st.radio("Choose Action", ["View Dashboard", "Edit Data Manually", "Upload Excel"])
    
    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.rerun()

df = load_data()

# --- MODE 1: UPLOAD EXCEL ---
if mode == "Upload Excel":
    st.subheader("📁 Upload New Data")
    uploaded_file = st.file_uploader("Upload your Excel sheet", type=["xlsx", "csv"])
    if uploaded_file:
        new_df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file)
        st.write("Preview of Uploaded Data:")
        st.dataframe(new_df.head())
        if st.button("Confirm & Update Dashboard"):
            save_data(new_df)
            st.success("Dashboard updated successfully!")

# --- MODE 2: EDIT MANUALLY ---
elif mode == "Edit Data Manually":
    st.subheader("📝 Live Data Entry")
    st.info("Edit the values in the table below and click Save.")
    edited_df = st.data_editor(df, num_rows="dynamic")
    if st.button("Save Changes"):
        save_data(edited_df)
        st.success("Data Saved!")

# --- MODE 3: VIEW DASHBOARD ---
else:
    # 1. KPI Top Row
    cols = st.columns(len(df))
    for i, row in df.iterrows():
        cols[i].metric(label=row['Metric'], value=row['Value'], help=f"Target: {row['Target']}")

    st.divider()

    # 2. Charts Row 1
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Defects by Module")
        # Sample data for visualization
        defect_data = pd.DataFrame({
            "Module": ["Login", "Payments", "Search", "Profile", "Checkout"],
            "Count": [5, 12, 3, 8, 2]
        })
        fig1 = px.bar(defect_data, x="Module", y="Count", color="Module", template="plotly_white")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("Test Execution Progress")
        exec_data = pd.DataFrame({
            "Status": ["Executed", "Passed", "Failed", "Blocked"],
            "Count": [100, 85, 10, 5]
        })
        fig2 = px.pie(exec_data, values="Count", names="Status", hole=0.4, 
                      color_discrete_map={'Passed':'#2ecc71', 'Failed':'#e74c3c', 'Blocked':'#f1c40f', 'Executed':'#3498db'})
        st.plotly_chart(fig2, use_container_width=True)

    # 3. Charts Row 2
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Defect Leakage Over Releases")
        leak_data = pd.DataFrame({
            "Release": ["v1.0", "v1.1", "v1.2", "v1.3"],
            "Leakage %": [8, 4, 6, 2]
        })
        fig3 = px.line(leak_data, x="Release", y="Leakage %", markers=True)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.subheader("Automation Coverage (%)")
        auto_data = pd.DataFrame({
            "Module": ["Core", "API", "UI", "Mobile"],
            "Coverage": [90, 80, 45, 30]
        })
        fig4 = px.bar(auto_data, x="Coverage", y="Module", orientation='h', color="Coverage")
        st.plotly_chart(fig4, use_container_width=True)