import streamlit as st
import main

# Store session state variables
if "sector_list" not in st.session_state:
    st.session_state.sector_list = []

if "selected_sectors" not in st.session_state:
    st.session_state.selected_sectors = []

if "selected_country" not in st.session_state:
    st.session_state.selected_country = None

if __name__ == "__main__":
    st.set_page_config(page_title="Category Selection", page_icon="📊")

    if "page" not in st.session_state:
        st.session_state.page = "home"

    if st.session_state.page == "home":
        main.category_selection()
    elif st.session_state.page == "upload":
        main.upload_excel()
