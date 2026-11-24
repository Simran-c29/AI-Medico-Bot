import streamlit as st

st.set_page_config(page_title="Streamlit Test")

st.title("Streamlit is Working! 🎉")

st.write("If you can see this, Streamlit is rendering correctly.")

st.success("UI Test Passed")

name = st.text_input("Enter your name")

if name:
    st.write(f"Hello, {name}!")