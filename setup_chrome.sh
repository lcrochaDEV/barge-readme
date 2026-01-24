#!/bin/bash
set -e  # Interrompe em caso de erro

echo "🚀 Iniciando configuração do ambiente Selenium..."

# Verifica se é root para usar apt-get, caso contrário tenta usar sudo
if [ "$(id -u)" -ne 0 ]; then
    SUDO="sudo"
else
    SUDO=""
fi

# 1. Atualiza e instala dependências básicas
$SUDO apt-get update && $SUDO apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    --no-install-recommends

# 2. Configura o repositório e instala o Google Chrome (apenas se não existir)
if ! command -v google-chrome &> /dev/null; then
    echo "🌐 Instalando Google Chrome..."
    curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | $SUDO apt-key add -
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | $SUDO tee /etc/apt/sources.list.d/google-chrome.list
    $SUDO apt-get update && $SUDO apt-get install -y google-chrome-stable --no-install-recommends
else
    echo "✅ Google Chrome já está instalado."
fi

# 3. Instala bibliotecas vitais para o modo Headless
$SUDO apt-get install -y \
    libnss3 \
    libxss1 \
    libasound2 \
    fonts-liberation \
    xdg-utils \
    --no-install-recommends

# 4. Limpeza para economizar espaço no runner
$SUDO rm -rf /var/lib/apt/lists/*

# 5. Instala as dependências do Python
# Usar --upgrade garante que o Selenium 4+ (que gerencia drivers sozinho) seja instalado
echo "🐍 Instalando dependências Python..."
pip install --upgrade pip
pip install --upgrade selenium

echo "✅ Ambiente configurado com sucesso!"