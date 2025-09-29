import streamlit as st
import time
import requests

st.title("Com rate limiting")

url = "http://127.0.0.1:5000"
status_area = st.empty()

now = time.time()
visitas = st.session_state.get("visitas", [])
visitas = [t for t in visitas if now - t < 60]

if len(visitas) >= 5:
    st.error("Muitas requisições (espere 1 min)")
else:
    if st.button("Executar"):
        visitas.append(now)
        st.session_state["visitas"] = visitas
        st.success("Executado!")

        status_area = st.empty()
        texto = ""
        for i in range(0,5):
            time.sleep(0.25)
            texto += "."
            status_area.info(texto)
        
        st.success(f"Executado! Visitas = {len(visitas)}")
        r = requests.get(url)
        st.code(r.text)


