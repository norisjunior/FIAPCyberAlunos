```
# CyberGuard - Simulador Educacional de Ransomware

Este projeto é um simulador educacional de ransomware, projetado para fins didáticos em ambientes controlados.

## Requisitos

Antes de executar o script Python, certifique-se de atender aos seguintes requisitos:

1. **Python 3.x**: Certifique-se de ter o Python 3 instalado em seu sistema.
   - Windows: [Baixe o Python](https://www.python.org/downloads/windows/)
   - Linux: Use o gerenciador de pacotes do seu distribuição (ex.: `sudo apt-get install python3`)
   - macOS: [Baixe o Python](https://www.python.org/downloads/mac-osx/)

2. Criar e ativar o ambiente virtual e atualizar o pip

```bash
python -m venv ransEnv
.\ransEnv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

3. **Pacote `cryptography`**: Este pacote é necessário para a criptografia e descriptografia dos arquivos.
   ```bash
   pip install cryptography python-dotenv tk
   ```

4. **Interface gráfica Tkinter**: O Tkinter é usado para criar a interface de usuário.
   - No Linux, você pode precisar instalar separadamente:
     ```bash
     sudo apt-get install python3-tk
     ```

5. **Diretório `finance`**: Crie um diretório chamado `finance` no mesmo local onde o script será executado. Coloque os arquivos que deseja simular a criptografia dentro deste diretório.

## Execução

1. Navegue até o diretório onde o script foi baixado.
2. Execute o script Python usando o comando:
   ```bash
   python3 cyberguard.py
   ```

## Notas Importantes

- Este script é apenas um simulador educacional e não deve ser usado em ambientes de produção.
- Apenas arquivos com extensões `.xls`, `.xlsx`, `.xsl`, `.docx`, `.pdf`, `.txt`, `.csv`, e `.pptx` serão criptografados.
- Após a execução, os arquivos serão renomeados com a extensão `.locked` e uma chave de descriptografia será gerada e salva em um arquivo chamado `key.rans`.

## Desenvolvedor

Este projeto foi desenvolvido por [Seu Nome] como parte de um estudo de caso sobre ransomware.
```