# Medidas para aumentar a segurança de um website (exemplo: Flask)

A seguir consta um conjunto de **controles simples**, apropriados para implementação em uma aplicação Flask. Cada item traz **explicação curta**, **por que é importante**, **como implementar (código mínimo)** e **referência**.

---

## 1) Rate limiting — limitar requisições por IP/usuário

**Por que:** evita abuso/DoS leve, brute-force e scraping excessivo.
**Como (rápido):** use a extensão `flask-limiter`. Ela é fácil de instalar e aplicar por rota ou globalmente.
**Código mínimo:**

```python
# app_rate_limit.py
from flask import Flask, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
# Limita por IP: 10 requisições por minuto por IP
limiter = Limiter(app, key_func=get_remote_address, default_limits=["10 per minute"])

@app.route("/")
def index():
    return "Olá — rota limitada a 10 req/min por IP"

@app.route("/login")
@limiter.limit("5 per minute")  # limite específico
def login():
    return "Página de login (limitada)"
```

**Observações:** para produção substitua o armazenamento em memória por Redis/outra store. ([Flask-Limiter][1])

---

## 2) Prevenção contra XSS (Cross-Site Scripting)

**Por que:** XSS permite execução de scripts no navegador de outro usuário — roubo de sessão, etc.
**Principais medidas simples:**

* **Escape** qualquer conteúdo inserido pelo usuário antes de renderizar ou use `{{ var }}` (escape automático de caracteres especiais).
* **Content Security Policy (CSP)** simples via header para reduzir impacto.

**Código mínimo (Flask + template):**

```python
# app_xss.py
from flask import Flask, render_template, make_response
app = Flask(__name__)

@app.route("/show")
def show():
    user_text = '<script>alert("XSS")</script>'  # exemplo vindo de DB/form
    # Jinja2 escapa por padrão: {{ user_text }} será seguro
    resp = make_response(render_template("show.html", text=user_text))
    # Cabeçalho CSP simples (evita execução de scripts externos)
    resp.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'"
    return resp
```

`templates/show.html`:

```html
<!doctype html>
<html>
  <body>
    <h1>Mensagem do usuário</h1>
    <p>{{ text }}</p>  <!-- Jinja escapa automaticamente -->
  </body>
</html>
```

**Observações:** evite usar `|safe` ou `autoescape false` a menos que saiba exatamente o que está tornando seguro. ([OWASP Cheat Sheet Series][2])

---

## 3) Proteção contra SQL Injection

**Por que:** SQLi permite leitura/modificação de dados indevidos e controle do BD.
**Princípios simples:** **nunca** formatar strings para montar queries; sempre usar **placeholders / parâmetros** (API do DB).

**Código mínimo com sqlite3 (exemplo de consulta segura):**

```python
# app_sql.py
import sqlite3
from flask import Flask, request, g

app = Flask(__name__)
DB = "exemplo.db"

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB)
    return g.db

@app.route("/user")
def get_user():
    user_id = request.args.get("id", "")
    db = get_db()
    # Usar placeholder "?" previne SQL injection
    cur = db.execute("SELECT name, email FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    return {"name": row[0], "email": row[1]} if row else ("Not found", 404)
```

**Se usar SQLAlchemy:** sempre ligue parâmetros via `filter_by()` / `query.filter()` em vez de string format. ([OWASP][3])

---

## 4) Validação mínima de entrada

**Por que:** reduzir superfície de ataque — por exemplo validar formatos (e-mail, inteiros) antes de usar valores.
**Sugestão:** para inputs simples, use `str.isdigit()`, regex básico ou bibliotecas de validação (WTForms / marshmallow). Exemplo curto:

```python
age = request.form.get("age","")
if not age.isdigit():
    return "age inválido", 400
age = int(age)
```

---

# Exemplo unido — pequeno app com rate limit + SQL safe

```python
# app_full.py
from flask import Flask, request, render_template, make_response, g
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sqlite3

app = Flask(__name__)
app.config["SECRET_KEY"] = "trocar_em_producao"
limiter = Limiter(app, key_func=get_remote_address, default_limits=["10 per minute"])

DB = "exemplo.db"
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB)
    return g.db

@app.route("/")
def index():
    return render_template("index.html")  # use {{ var }} em templates — Jinja escapa por padrão

@app.route("/user")
@limiter.limit("5 per minute")
def user():
    uid = request.args.get("id","")
    if not uid.isdigit():              # validação simples
        return ("id inválido", 400)
    db = get_db()
    cur = db.execute("SELECT name FROM users WHERE id = ?", (uid,))
    row = cur.fetchone()
    return {"name": row[0]} if row else ("Not found", 404)

if __name__ == "__main__":
    app.run()
```

# Referências (principais, consultáveis)

* OWASP XSS Prevention Cheat Sheet. ([OWASP Cheat Sheet Series][2])
* OWASP SQL Injection / Testing for SQL Injection. ([OWASP][3])
* Flask-Limiter docs (rate limiting). ([Flask-Limiter][1])
* Flask templating / Jinja2 autoescape (docs). ([flask.palletsprojects.com][4])

---

[1]: https://flask-limiter.readthedocs.io/?utm_source=chatgpt.com "Flask-Limiter {4.0.0}"
[2]: https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html?utm_source=chatgpt.com "Cross Site Scripting Prevention - OWASP Cheat Sheet Series"
[3]: https://owasp.org/www-community/attacks/SQL_Injection?utm_source=chatgpt.com "SQL Injection"
[4]: https://flask.palletsprojects.com/en/stable/templating/?utm_source=chatgpt.com "Templates — Flask Documentation (3.1.x)"
[5]: https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/05-Testing_for_SQL_Injection?utm_source=chatgpt.com "Testing for SQL Injection"
