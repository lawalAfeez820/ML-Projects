import streamlit as st
from predict_page import show_predict_page
from explore_page import show_explore_page

new_page=st.sidebar.selectbox("Predict or Explore",("Predict","Explore"))
if new_page=="Predict":
    show_predict_page()
else:
    show_explore_page()