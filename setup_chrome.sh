#!/bin/bash

# Atualiza os pacotes e instala dependências básicas
apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    --no-install-recommends

# Adiciona a chave e o repositório do Google Chrome
curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list

# Instala o Chrome e dependências de renderização
apt-get update && apt-get install -y \
    google-chrome-stable \
    libnss3 \
    libgconf-2-4 \
    libxss1 \
    libasound2 \
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils \
    --no-install-recommends

# Limpa o cache para reduzir o tamanho da imagem/ambiente
rm -rf /var/lib/apt/lists/*

# Instala bibliotecas Python
pip install selenium