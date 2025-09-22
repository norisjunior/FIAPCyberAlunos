# flask_vuln.py
from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "Use /fetch?url=http://... para testar SSRF"

@app.route("/fetch")
def fetch():
    url = request.args.get("url")
    r = requests.get(url)  # sem restrição → vulnerável
    return r.text

if __name__ == "__main__":
    app.run(port=5001)  # serviço exposto ao atacante
