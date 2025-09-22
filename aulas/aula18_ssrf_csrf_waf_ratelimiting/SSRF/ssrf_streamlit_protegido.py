# streamlit_protegido.py
import streamlit as st
import requests
from urllib.parse import urlparse

ALLOWED_HOSTS = {"example.com"}  # só este é aceito

st.title("SSRF Demo - Protegido")

url = st.text_input("Digite uma URL")
if st.button("Buscar"):
    u = urlparse(url)
    if u.scheme not in {"http", "https"}:
        st.error("Protocolo não permitido")
    elif u.hostname not in ALLOWED_HOSTS:
        st.error("Host não permitido")
    else:
        r = requests.get(url, timeout=3)
        st.code(r.text)
