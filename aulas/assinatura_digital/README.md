# Assinatura Digital (exemplo com streamlit)

Simulação didática de **assinatura digital com chaves pública e privada (RSA)**:

1. **`app1_assinatura_digital_TRANSMISSOR.py`** → Gera as chaves e assina o texto.
2. **`app2_assinatura_digital_RECEPTOR.py`** → Verifica se a assinatura é autêntica.


---

## Instalação

### Criar ambiente virtual

```bash
python -m venv venv
```

### Ativar o ambiente

```bash
# Windows
venv\Scripts\activate
```

### Instalar dependências

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## Execução dos Aplicativos

### App 1 — TRANSMISSOR (Assinatura)

```bash
streamlit run app1_assinatura_digital_TRANSMISSOR.py
```

**Funções:**

* Gera as chaves RSA (privada e pública);
* Mostra o hash (SHA-256) do texto;
* Cria a assinatura digital;
* Permite baixar a chave pública (.pem).

**Esquema visual:**
1. Clique em “Gerar Chaves RSA”
2. Digite o texto
3. Clique em “Gerar Assinatura Digital”
4. Baixe o arquivo `chave_publica.pem`

---

### App 2 — DESTINATÁRIO (Verificação)

***Dica:*** use a opção "split terminal" do VSCode

```bash
streamlit run app2_assinatura_digital_RECEPTOR.py
```

**Funções:**

* Faz upload da chave pública (.pem);
* Recebe o texto e a assinatura em hexadecimal;
* Verifica se a mensagem é autêntica e não foi alterada.

**Esquema visual:**
1. Faça upload da `chave_publica.pem`
2. Cole o texto original ou modificado
3. Cole a assinatura digital
4. Clique em "Verificar Assinatura"

|> Se o texto tiver sido alterado, o app mostrará uma mensagem de **alerta vermelho** indicando que a assinatura é inválida.

