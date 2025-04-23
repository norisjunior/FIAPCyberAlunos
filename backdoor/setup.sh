#!/bin/bash

echo "---> Atualizando pacotes e instalando dependências..."
sudo apt update
sudo apt install -y python3-pip openssl python3-flask

echo "---> Criando diretórios necessários..."
mkdir -p upload
mkdir -p certs
mkdir -p templates

echo "---> Gerando certificado digital autoassinado..."
openssl req -new -x509 -days 365 -nodes -out certs/server.crt -keyout certs/server.key -subj "/C=BR/ST=SP/L=SaoPaulo/O=CyberGuard/OU=TI/CN=localhost"

echo "---> Iniciando servidor Flask com HTTPS na porta 443..."
sudo python3 app.py
