# streamlit_rate_vuln.py
import streamlit as st

st.title("Rate Limiting Demo - Vulnerável")

# inicializa contador na sessão
if "contador" not in st.session_state:
    st.session_state.contador = 0

if st.button("Executar"):
    st.session_state.contador += 1
    st.success(f"Executado! Contador = {st.session_state.contador}")
