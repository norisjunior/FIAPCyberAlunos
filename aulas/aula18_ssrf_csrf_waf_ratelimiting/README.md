# Como executar os exemplos de SSRF e Rate Limiting

Este material contém **exemplos práticos de vulnerabilidades** (SSRF e falta de Rate Limiting) e suas respectivas **versões protegidas**, usando **Flask** e **Streamlit**.
A ideia é que você execute os dois lados: primeiro o **sistema interno** (com o segredo) e depois os **aplicativos externos** (vulneráveis ou protegidos).

---

## 1. Criar e ativar o ambiente virtual

```bash
python -m venv cyberEnv
.\cyberEnv\Scripts\Activate.ps1   # Windows PowerShell
```

---

## 2. Instalar dependências

```bash
python -m pip install --upgrade pip
pip install flask streamlit requests
```

---

## 3. Executar os exemplos

### 3.1 Sistema interno (sempre inicie este primeiro)

Este é o **sistema interno** que guarda o segredo.

```bash
cd SISTEMA_INTERNO
python sistema_interno.py
```

Acesse diretamente para conferir:

```
http://127.0.0.1:5000/segredo.txt
```

---

### 3.2 SSRF

#### 3.2.1 SSRF Vulnerável (Flask)

**FLASK** - Servidor vulnerável

Abra um novo terminal e execute:

```bash
python SSRF\ssrf_flask_vuln.py
```

Ataque via navegador ou curl:

```
http://127.0.0.1:5001/fetch?url=http://127.0.0.1:5000/segredo.txt
```

!!! O segredo é exposto.

Adicional: acesse qualquer website em vez de http://127.0.0.1:5000/segredo.txt

*Pare o servidor vulnerável inicializado.*

---

#### 3.2.2 SSRF Protegido (Flask)

**FLASK** - Servidor protegido

Inicie o servidor com proteção à SSRF:

```bash
python SSRF\ssrf_flask_protegido.py
```

Teste:

* Não acessa (bloqueado):

```
http://127.0.0.1:5002/fetch?url=http://127.0.0.1:5000/segredo.txt
```

* Acessa (porque *está* na allowlist):

```
http://127.0.0.1:5002/fetch?url=https://example.com
```

* Não Acessa (porque *não está* na allowlist):
```
http://127.0.0.1:5002/fetch?url=https://www.fiap.com.br
```

*Pare o servidor protegido inicializado.*

---

#### 3.2.3 SSRF Vulnerável (Streamlit)

**STREAMLIT** - Inicie o servidor vulnerável

```bash
streamlit run SSRF\ssrf_streamlit_vuln.py
```

Digite no campo URL do website iniciado:

```
http://127.0.0.1:5000/segredo.txt
```

!!! O segredo é exposto.

Adicional: acesse qualquer website em vez de http://127.0.0.1:5000/segredo.txt

*Pare o servidor vulnerável inicializado.*


---

#### 3.2.4 SSRF Protegido (Streamlit)

**STREAMLIT** - Inicie o servidor protegido

```bash
streamlit run SSRF\ssrf_streamlit_protegido.py
```

Digite no campo:

```
http://127.0.0.1:5000/segredo.txt
```

<> Bloqueado.

*Pare o servidor protegido inicializado.*

---

### 3.3 Rate Limiting

#### 3.3.1 Vulnerável (Flask)

```bash
python RATE_LIMIT\rate_flask_vuln.py
```

Teste com várias requisições rápidas:

```bash
http://127.0.0.1:5001
```

-> Todas retornam `200`.

---

#### 3.3.2 Protegido (Flask)

```bash
python RATE_LIMIT\rate_flask_protegido.py
```

Teste com várias requisições rápidas:

```bash
http://127.0.0.1:5001
```

--> As primeiras retornam `200`, as seguintes `429`.

---

#### 3.3.3 Vulnerável (Streamlit)

```bash
streamlit run RATE_LIMIT\rate_streamlit_vuln.py
```

--> Cada clique no botão soma +1 no contador, sem limite.

---

#### 3.3.4 Protegido (Streamlit)

```bash
streamlit run RATE_LIMIT\rate_streamlit_protegido.py
```

--> Após 5 cliques em menos de 1 minuto, aparece a mensagem:
**"Muitas requisições (espere 1 min)"**

---

## Resumo

* **SSRF**: mostra como um sistema externo pode abusar de endpoints internos (pegando `segredo.txt`): solução: **allowlist** + **bloqueio de hosts internos**.
* **Rate Limiting**: mostra como requisições excessivas podem derrubar o sistema: solução: **limitar por tempo/IP/sessão**.
