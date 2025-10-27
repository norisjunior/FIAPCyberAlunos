# Auditoria de Redes Wireless com Aircrack-ng e Hashcat

**Aviso Legal:** O uso dessas ferramentas para monitorar ou atacar redes sem fio das quais você **não possui autorização explícita** é ilegal e antiético. Use-as apenas em seus próprios equipamentos (ambiente de teste) ou redes com permissão documentada para fins de aprendizado ou auditoria de segurança.

-----

## 1\. Captura do Handshake

**Confirmar:** Verifique se a mensagem **`WPA Handshake: <BSSID do AP>`** apareceu na tela do `airodump-ng`. Interrompa o `airodump-ng` e desative o modo monitor (`sudo airmon-ng stop wlan0mon`).

-----

## 2\. Quebrar a Senha com `hashcat`

### 2.1. Converter o Arquivo `.cap` para o Formato Hashcat

O Hashcat requer que o *handshake* seja convertido. Use a ferramenta `hcxpcapngtool` para o formato `.hash` (melhor para Hashcat). Para instalar a ferramenta `hcxpcapngtool`:
```bash
sudo apt update

sudo apt install -y hcxtools
```

E então é possível executar:

```bash
hcxpcapngtool -o <arquivo_hash_saida>.hash <arquivo_captura>.cap
```

  * **Exemplo:** `hcxpcapngtool -o myhash.hash capture_target-01.cap`

### 2.2. Ataque de Dicionário (Se você não souber nada)

Este método testa uma lista inteira de palavras.

```bash
hashcat -m 22000 <arquivo_hash>.hash -a 0 <arquivo_dicionario>.txt
```

  * **Parâmetros:**
      * `-m 22000`: Modo para WPA/WPA2.
      * `-a 0`: Modo de ataque Dicionário.
      * `rockyou.txt`: Exemplo de lista de palavras (`/usr/share/wordlists/rockyou.txt`).

### 2.3. Ataque de Máscara (Se você souber parte da senha)

Este método é ideal para testar padrões, como quando você sabe o comprimento total e alguns caracteres. O Hashcat usa caracteres especiais para representar tipos de caracteres desconhecidos:

| Caractere | Significado | Exemplo |
| :--- | :--- | :--- |
| `?l` | Letras minúsculas (`a` - `z`) | `?l?l` = aa, ab, ac... |
| `?u` | Letras maiúsculas (`A` - `Z`) | |
| `?d` | Dígitos (`0` - `9`) | |
| `?s` | Símbolos (`!@#$%...`) | |
| `?a` | Todos os caracteres acima (padrão) | |

#### Cenário: Senha de 12 caracteres, sabendo os 6 primeiros

**Sua máscara:** Se a senha tem **12 caracteres**, e você sabe que os 6 primeiros são `senha1`, os 6 caracteres restantes são desconhecidos. Se você suspeitar que os 6 restantes são apenas dígitos, sua máscara seria:

`senha1?d?d?d?d?d?d`

**Comando do Hashcat (Ataque de Máscara):**

```bash
hashcat -m 22000 <arquivo_hash>.hash -a 3 <máscara>
```

  * **Exemplo:**

    ```bash
    hashcat -m 22000 myhash.hash -a 3 senha1?d?d?d?d?d?d
    ```
      * `-m 22000`: 22000 é o modo de descoberta de hash de senhas capturadas pelo airmon-ng
      * `-a 3`: Define o modo de ataque como **Máscara**.
      * `senha1?d?d?d?d?d?d`: A máscara diz ao Hashcat para testar todas as combinações de 6 dígitos após `senha1`.

**Dica:** O ataque de máscara é significativamente mais rápido que o ataque de força bruta total, pois reduz drasticamente o espaço de chaves a ser testado.

-----

**Resultado:** Se a senha for encontrada, ela será exibida no terminal e salva no arquivo **`hashcat.potfile`**.