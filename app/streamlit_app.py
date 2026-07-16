import streamlit as st
from src import logging
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "url"

st.title("Student Placement Prediction")

with st.form("placement_form"):

    ssc_p = st.number_input(
        "SSC Percentage",
        min_value=0.0,
        max_value=100.0
    )

    ssc_b = st.selectbox(
        "SSC Board",
        ["Central", "Others"]
    )

    hsc_p = st.number_input(
        "HSC Percentage",
        min_value=0.0,
        max_value=100.0
    )

    hsc_b = st.selectbox(
        "HSC Board",
        ["Central", "Others"]
    )

    hsc_s = st.selectbox(
        "HSC Stream",
        ["Commerce", "Science", "Arts"]
    )

    degree_p = st.number_input(
        "Degree Percentage",
        min_value=0.0,
        max_value=100.0
    )

    degree_t = st.selectbox(
        "Degree Type",
        ["Sci&Tech", "Comm&Mgmt", "Others"]
    )

    workex = st.selectbox(
        "Work Experience",
        ["Yes", "No"]
    )

    etest_p = st.number_input(
        "Employability Test Percentage",
        min_value=0.0,
        max_value=100.0
    )

    specialisation = st.selectbox(
        "MBA Specialisation",
        ["Mkt&HR", "Mkt&Fin"]
    )

    mba_p = st.number_input(
        "MBA Percentage",
        min_value=0.0,
        max_value=100.0
    )

    submit = st.form_submit_button("Predict")


if submit:

    input_data = {
        "ssc_p": ssc_p,
        "ssc_b": ssc_b,
        "hsc_p": hsc_p,
        "hsc_b": hsc_b,
        "hsc_s": hsc_s,
        "degree_p": degree_p,
        "degree_t": degree_t,
        "workex": workex,
        "etest_p": etest_p,
        "specialisation": specialisation,
        "mba_p": mba_p
    }
    logging.info('try to send post request')
    try:
        response = requests.post(
            API_URL,
            json=input_data
        )

        if response.status_code == 200:
            result = response.json()
            st.success(f"Prediction: {result['status']}")
            logging.info('post is sent successfully')
        else:
            logging.error(response.text)
            st.error(response.text)

    except Exception as e:
        st.error(f"API connection failed: {e}")
        logging.exception(e)
