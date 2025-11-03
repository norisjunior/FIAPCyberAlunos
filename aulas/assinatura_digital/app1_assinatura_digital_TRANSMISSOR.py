# assinatura_app_1.py (versão simples, com persistência leve)
import streamlit as st
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

st.title(" Assinatura Digital - Parte 1 (Remetente)")
st.write("Gera chaves RSA, assina o texto e salva a chave pública (.pem).")

# --- MANTER DADOS NA MEMÓRIA ---
if "private_key" not in st.session_state:
    st.session_state.private_key = None
if "public_key" not in st.session_state:
    st.session_state.public_key = None
if "assinatura" not in st.session_state:
    st.session_state.assinatura = None
if "hash" not in st.session_state:
    st.session_state.hash = None

# --- GERAR CHAVES ---
if st.button("Gerar Chaves RSA"):
    key = RSA.generate(2048)
    st.session_state.private_key = key.export_key()
    st.session_state.public_key = key.publickey().export_key()
    st.success(" Chaves geradas com sucesso!")

# Exibir e baixar chave pública (se existir)
if st.session_state.public_key:
    st.download_button(" Baixar Chave Pública (.pem)",
                       data=st.session_state.public_key,
                       file_name="chave_publica.pem")
    st.text_area(" Chave Privada (mantenha em sigilo!)",
                 st.session_state.private_key.decode(), height=200)

# --- DIGITAR TEXTO ---
texto = st.text_area(" Escreva o texto que deseja assinar:", "")

# --- GERAR ASSINATURA ---
if st.button("Gerar Assinatura Digital"):
    if st.session_state.private_key is None:
        st.error(" Gere as chaves primeiro!")
    elif not texto.strip():
        st.warning("Digite um texto antes de assinar!")
    else:
        private_key = RSA.import_key(st.session_state.private_key)
        hash_doc = SHA256.new(texto.encode())
        assinatura = pkcs1_15.new(private_key).sign(hash_doc)
        st.session_state.assinatura = assinatura
        st.session_state.hash = hash_doc.hexdigest()

# --- EXIBIR RESULTADOS ---
if st.session_state.hash:
    st.subheader(" Impressão Digital (SHA-256)")
    st.code(st.session_state.hash, language="plaintext")

if st.session_state.assinatura:
    st.subheader(" Assinatura Digital (hexadecimal)")
    st.text_area("Assinatura (hex)", st.session_state.assinatura.hex(), height=150)
