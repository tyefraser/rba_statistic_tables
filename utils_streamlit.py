import streamlit as st

def streamlit_error_stop(
        error_text
):
    st.error(error_text)
    st.stop()

    return 0