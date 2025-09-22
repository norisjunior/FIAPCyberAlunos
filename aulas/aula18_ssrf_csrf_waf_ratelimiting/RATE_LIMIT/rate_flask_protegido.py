from flask import Flask, request, abort
import time

app = Flask(__name__)
visitas = {}

@app.before_request
def rate_limit():
    ip = request.remote_addr or "unknown"
    now = time.time()
    janela = 60   # segundos
    limite = 5    # máx 5 req/min

    visitas.setdefault(ip, [])
    visitas[ip] = [t for t in visitas[ip] if now - t < janela]

    if len(visitas[ip]) >= limite:
        abort(429, "Muitas requisições, tente mais tarde.")

    visitas[ip].append(now)

@app.route("/")
def home():
    return "Olá, com rate limiting!"

if __name__ == "__main__":
    app.run(debug=True, port=5001)
