import streamlit as st
import pandas as pd

# -----------------------------
# STYLE (makes it look better)
# -----------------------------
st.markdown("""
<style>
.stApp {
    background-color: #f5f7fa;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# PAGE SETUP
# -----------------------------
st.set_page_config(page_title="JustinFloors Job Tracker", layout="wide")

st.title("JustinFloors Job Tracker")

# -----------------------------
# SESSION DATA (fake database)
# -----------------------------
if "jobs" not in st.session_state:
    st.session_state.jobs = pd.DataFrame([
        {"Job ID": 1, "Customer": "Avery Thompson", "Status": "New Lead", "Install Date": "", "Materials": "Not Ordered"},
        {"Job ID": 2, "Customer": "Jordan Mitchell", "Status": "Materials Ordered", "Install Date": "", "Materials": "Ordered"},
        {"Job ID": 3, "Customer": "Casey Reynolds", "Status": "Installer Scheduled", "Install Date": "2026-04-05", "Materials": "Received"},
    ])

jobs = st.session_state.jobs

# -----------------------------
# DASHBOARD METRICS
# -----------------------------
st.header("Dashboard")

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

# -----------------------------
# FILTERS
# -----------------------------
st.subheader("Filter Jobs")

status_filter = st.selectbox(
    "Filter by Status",
    ["All"] + list(jobs["Status"].unique())
)

if status_filter != "All":
    filtered_jobs = jobs[jobs["Status"] == status_filter]
else:
    filtered_jobs = jobs

st.dataframe(filtered_jobs, use_container_width=True)

# -----------------------------
# WAITING ON MATERIALS
# -----------------------------
st.subheader("Jobs Waiting on Materials")

waiting_jobs = jobs[jobs["Materials"] != "Received"]
st.dataframe(waiting_jobs, use_container_width=True)

# -----------------------------
# UPCOMING INSTALLS
# -----------------------------
st.subheader("Upcoming Installs")

upcoming = jobs[
    (jobs["Install Date"] != "") &
    (jobs["Status"] == "Installer Scheduled")
]

st.dataframe(upcoming, use_container_width=True)

# -----------------------------
# INSIGHTS (this impresses professors)
# -----------------------------
st.subheader("Insights")

if waiting > 0:
    st.warning(f"{waiting} jobs are waiting on materials. This may delay installs.")
else:
    st.success("All jobs have materials ready!")

# -----------------------------
# ADD JOB
# -----------------------------
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
        st.success("Job added! Refresh to see update.")

# -----------------------------
# UPDATE JOB
# -----------------------------
st.subheader("Update Job Status")

job_id = st.number_input("Enter Job ID to Update", min_value=1, step=1)

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
        st.error("Job ID not found")
