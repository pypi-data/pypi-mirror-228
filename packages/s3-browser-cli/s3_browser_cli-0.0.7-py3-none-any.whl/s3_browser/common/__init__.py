import streamlit as st


def safe_update_page_args(**kwargs):
    current_params = st.experimental_get_query_params()
    current_params.update(kwargs)
    st.experimental_set_query_params(**current_params)


def safe_clear_page_args(*args):
    current_params = st.experimental_get_query_params()
    for arg in args:
        if arg in current_params.keys():
            if arg in ["current_s3"]:
                continue

            current_params.pop(arg)
    st.experimental_set_query_params(**current_params)


def query_text_input(label: str, key: str, **kwargs):
    query = st.experimental_get_query_params()
    query_value = (query.get(key) or [""])[0]
    if key in st.session_state and query_value != st.session_state[key]:
        query_value = st.session_state[key]
        safe_update_page_args(**{key: query_value})
    ret = st.text_input(label, query_value, key=key, **kwargs)
    return ret.strip() if ret else ret


def safe_get_query_value(key: str) -> str:
    query = st.experimental_get_query_params()
    query_value = (query.get(key) or [""])[0]
    return query_value
