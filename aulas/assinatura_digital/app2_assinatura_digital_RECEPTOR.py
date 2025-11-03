# assinatura_app_2.py
import streamlit as st
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import binascii

st.title(" Verificação de Assinatura Digital - Parte 2 (Destinatário)")
st.write("Faça upload da chave pública, insira o texto e a assinatura para verificar autenticidade.")

# Upload da chave pública
chave_pub_file = st.file_uploader(" Faça upload da chave pública (.pem)", type=["pem"])

# Texto recebido
texto = st.text_area(" Texto recebido:", "")

# Assinatura recebida
assinatura_hex = st.text_area(" Assinatura recebida (hexadecimal):", "")

# Verificação
if st.button("Verificar Assinatura"):
    if not chave_pub_file or not texto.strip() or not assinatura_hex.strip():
        st.warning(" Preencha todos os campos e envie a chave pública!")
    else:
        try:
            # 1) Importa a chave pública
            public_key = RSA.import_key(chave_pub_file.read())

            # 2) Converte assinatura de hexadecimal para bytes
            assinatura_bytes = binascii.unhexlify(assinatura_hex.strip())

            # 3) Calcula o hash do texto recebido
            hash_recebido = SHA256.new(texto.encode())

            # 4) Verifica assinatura com a chave pública
            pkcs1_15.new(public_key).verify(hash_recebido, assinatura_bytes)

            # --- Exibição passo a passo ---
            st.success(" Documento AUTÊNTICO e ASSINATURA VÁLIDA!")

            st.write(" **Chave pública (PEM):**")
            st.code(public_key.export_key().decode(), language="plaintext")

            st.write(" **Assinatura (hex → bytes):**")
            st.code(assinatura_hex.strip(), language="plaintext")

            st.write(" **Hash calculado (SHA-256):**")
            hdemo = SHA256.new(texto.encode()).hexdigest()
            st.code(hdemo, language="plaintext")

        except (ValueError, TypeError, binascii.Error):
            st.error(" Assinatura inválida ou mensagem adulterada!")
