import streamlit as st
import pandas as pd

# -----------------------------
# STYLE (BIG visual upgrade)
# -----------------------------
st.markdown("""
<style>
.stApp {
    background-color: #f4f6f9;
}

.block-container {
    padding-top: 2rem;
}

h1, h2, h3 {
    color: #1f2937;
}

div[data-testid="stMetric"] {
    background-color: white;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="JustinFloors Job Tracker", layout="wide")

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("🏠 JustinFloors")
page = st.sidebar.radio("Navigation", ["Dashboard", "Manage Jobs"])

# -----------------------------
# SESSION DATA
# -----------------------------
if "jobs" not in st.session_state:
    st.session_state.jobs = pd.DataFrame([
        {"Job ID": 1, "Customer": "Avery Thompson", "Status": "New Lead", "Install Date": "", "Materials": "Not Ordered"},
        {"Job ID": 2, "Customer": "Jordan Mitchell", "Status": "Materials Ordered", "Install Date": "", "Materials": "Ordered"},
        {"Job ID": 3, "Customer": "Casey Reynolds", "Status": "Installer Scheduled", "Install Date": "2026-04-05", "Materials": "Received"},
    ])

jobs = st.session_state.jobs

# -----------------------------
# COLOR FUNCTION
# -----------------------------
def color_status(val):
    if val == "New Lead":
        return "background-color: #dbeafe"
    elif val == "Materials Ordered":
        return "background-color: #fef3c7"
    elif val == "Installer Scheduled":
        return "background-color: #d1fae5"
    elif val == "Install Complete":
        return "background-color: #bbf7d0"
    else:
        return ""

# -----------------------------
# DASHBOARD
# -----------------------------
if page == "Dashboard":

    st.title("📊 Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Jobs", len(jobs))

    with col2:
        waiting = len(jobs[jobs["Materials"] != "Received"])
        st.metric("Waiting on Materials", waiting)

    with col3:
        scheduled = len(jobs[jobs["Status"] == "Installer Scheduled"])
        st.metric("Scheduled Installs", scheduled)

    st.divider()

    # FILTER
    status_filter = st.selectbox(
        "Filter by Status",
        ["All"] + list(jobs["Status"].unique())
    )

    if status_filter != "All":
        filtered_jobs = jobs[jobs["Status"] == status_filter]
    else:
        filtered_jobs = jobs

    st.subheader("All Jobs")

    st.dataframe(filtered_jobs, use_container_width=True)

    colA, colB = st.columns(2)

    with colA:
        st.subheader("🚨 Waiting on Materials")
        waiting_jobs = jobs[jobs["Materials"] != "Received"]
        st.dataframe(waiting_jobs, use_container_width=True)

    with colB:
        st.subheader("📅 Upcoming Installs")
        upcoming = jobs[
            (jobs["Install Date"] != "") &
            (jobs["Status"] == "Installer Scheduled")
        ]
        st.dataframe(upcoming, use_container_width=True)

    st.divider()

    if waiting > 0:
        st.warning(f"{waiting} jobs are waiting on materials — potential delays.")
    else:
        st.success("All jobs ready to go!")

# -----------------------------
# MANAGE JOBS
# -----------------------------
elif page == "Manage Jobs":

    st.title("⚙️ Manage Jobs")

    st.subheader("Add New Job")

    with st.form("add_job"):
        customer = st.text_input("Customer Name")
        status = st.selectbox("Status", ["New Lead", "Qualified", "Measured", "Materials Ordered", "Installer Scheduled"])
        install_date = st.text_input("Install Date")
        materials = st.selectbox("Materials Status", ["Not Ordered", "Ordered", "Received"])

        submitted = st.form_submit_button("Add Job")

        if submitted and customer:
            new_row = {
                "Job ID": len(jobs) + 1,
                "Customer": customer,
                "Status": status,
                "Install Date": install_date,
                "Materials": materials
            }
            st.session_state.jobs = pd.concat([jobs, pd.DataFrame([new_row])], ignore_index=True)
            st.success("Job added!")

    st.divider()

    st.subheader("Update Job Status")

    job_id = st.number_input("Job ID", min_value=1, step=1)

    new_status = st.selectbox(
        "New Status",
        ["New Lead", "Qualified", "Measured", "Materials Ordered", "Installer Scheduled", "Install Complete"]
    )

    if st.button("Update"):
        if job_id in jobs["Job ID"].values:
            st.session_state.jobs.loc[
                st.session_state.jobs["Job ID"] == job_id, "Status"
            ] = new_status
            st.success("Job updated!")
        else:
            st.error("Job not found")
