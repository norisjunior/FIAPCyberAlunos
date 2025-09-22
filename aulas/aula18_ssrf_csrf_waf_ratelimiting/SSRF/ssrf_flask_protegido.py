# flask_protegido.py
from flask import Flask, request, abort
import requests
from urllib.parse import urlparse

app = Flask(__name__)
ALLOWED_HOSTS = {"example.com"}  # só permite esse host

@app.route("/")
def home():
    return "PROTEÇÃO CONTRA SSRF ATIVA: Tente usar /fetch?url=http://... para testar SSRF. Link de exemplo para avaliar a proteção contra SSRF: http://127.0.0.1:5002/fetch?url=http://127.0.0.1:5000/segredo.txt"

@app.route("/fetch")
def fetch():
    url = request.args.get("url")
    u = urlparse(url)

    if u.scheme not in {"http", "https"}:
        abort(400, "Protocolo não permitido")
    if u.hostname not in ALLOWED_HOSTS:
        abort(403, "Host não permitido")

    r = requests.get(url, timeout=3)
    return r.text

if __name__ == "__main__":
    app.run(port=5002)  # serviço protegido
