import streamlit as st
import pandas as pd

st.subheader("All Jobs")
st.dataframe(jobs, use_container_width=True)

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

    if submitted:
        new_row = {
            "Job ID": len(jobs) + 1,
            "Customer": customer,
            "Status": status,
            "Install Date": install_date,
            "Materials": materials
        }
        st.session_state.jobs = pd.concat([jobs, pd.DataFrame([new_row])], ignore_index=True)
        st.success("Job added!")

# -----------------------------
# UPDATE JOB
# -----------------------------
st.subheader("Update Job Status")

job_id = st.number_input("Enter Job ID to Update", min_value=1, step=1)

new_status = st.selectbox("New Status", ["New Lead", "Qualified", "Measured", "Materials Ordered", "Installer Scheduled", "Install Complete"])

if st.button("Update"):
    st.session_state.jobs.loc[st.session_state.jobs["Job ID"] == job_id, "Status"] = new_status
    st.success("Job updated!")
