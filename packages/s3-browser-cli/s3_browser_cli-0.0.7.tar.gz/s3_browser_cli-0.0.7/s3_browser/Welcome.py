import streamlit as st
from s3_browser.common.s3_client import get_s3_client_list

st.set_page_config(page_title="Welcome to the s3_browser", layout="wide")

st.markdown("## Welcome to the s3_browser")

s3_client_list = get_s3_client_list()
selected_index = 0
current_s3 = st.experimental_get_query_params().get("current_s3", [""])[0]

if current_s3:
    for i, k in enumerate(s3_client_list):
        if current_s3 == k["name"]:
            selected_index = i
            break

selected_s3 = st.selectbox(
    "Current S3 config", options=s3_client_list, index=selected_index
)
st.experimental_set_query_params(**{"current_s3": selected_s3["name"]})
