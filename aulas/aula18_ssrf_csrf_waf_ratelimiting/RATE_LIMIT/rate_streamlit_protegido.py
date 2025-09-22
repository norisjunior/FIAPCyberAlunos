import streamlit as st
import time

st.title("Com rate limiting")

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
