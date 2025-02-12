import streamlit as st
import main_v2

# Store session state variables
if "sector_list" not in st.session_state:
    st.session_state.sector_list = []

if "selected_sectors" not in st.session_state:
    st.session_state.selected_sectors = []

if "selected_country" not in st.session_state:
    st.session_state.selected_country = None

if __name__ == "__main__":
    st.set_page_config(page_title="Lead Gen v2", page_icon="📊")

    if "page" not in st.session_state:
        st.session_state.page = "home"

    if st.session_state.page == "home":
        main_v2.category_selection()
    elif st.session_state.page == "upload":
        main_v2.upload_excel()
