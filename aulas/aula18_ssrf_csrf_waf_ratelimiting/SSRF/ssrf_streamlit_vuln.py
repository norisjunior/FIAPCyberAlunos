# streamlit_vuln.py
import streamlit as st
import requests

st.title("SSRF Demo - Vulnerável")

url = st.text_input("Digite uma URL")
if st.button("Buscar"):
    r = requests.get(url)
    st.code(r.text)
