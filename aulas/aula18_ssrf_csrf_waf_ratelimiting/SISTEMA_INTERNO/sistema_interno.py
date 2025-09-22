# sistema_interno.py
from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "Sistema interno. Acesso limitado aos funcionários e demais colaboradores."

@app.route("/segredo.txt")
def segredo():
    return open("segredo.txt").read()

@app.route("/fetch")
def fetch():
    url = request.args.get("url")
    r = requests.get(url)
    return r.text

if __name__ == "__main__":
    app.run(debug=True, port=5000)
