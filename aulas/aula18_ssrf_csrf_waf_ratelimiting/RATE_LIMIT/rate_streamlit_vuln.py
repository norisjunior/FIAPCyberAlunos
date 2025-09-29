# streamlit_rate_vuln.py
import streamlit as st
import requests
import time

st.title("Rate Limiting Demo - Vulnerável")

url = "http://127.0.0.1:5000"
status_area = st.empty()

# inicializa contador na sessão
if "contador" not in st.session_state:
    st.session_state.contador = 0

if st.button("Executar"):
    status_area = st.empty()
    texto = ""
    for i in range(0,5):
        time.sleep(0.5)
        texto += "."
        status_area.info(texto)
    
    st.session_state.contador += 1
    st.success(f"Executado! Contador = {st.session_state.contador}")
    r = requests.get(url)
    st.code(r.text)

