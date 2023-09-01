import streamlit as st
from common.s3_client import get_s3_client

st.set_page_config(page_title="Bucket Policy", page_icon="", layout="wide")

with st.spinner("Loading"):
    buckets = [f"s3://{item}/" for item in get_s3_client().list_buckets()]

bucket = st.selectbox("Please select a bucket", buckets)

if not bucket:
    st.error("Empty bucket list")
    st.stop()

try:
    result = get_s3_client().get_bucket_policy(bucket)
    st.json(result["Policy"])
except Exception as e:
    st.info(f"Empty policy {e}")
