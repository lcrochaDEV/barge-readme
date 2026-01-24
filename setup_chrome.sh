#!/bin/bash
set -e  # Interrompe em caso de erro

echo "🚀 Iniciando configuração do ambiente Selenium..."

# 0. Limpa travas do APT (Evita erro 100)
sudo rm -f /var/lib/dpkg/lock-frontend
sudo rm -f /var/lib/apt/lists/lock

# Define SUDO se necessário
SUDO=$(command -v sudo)

# 1. Atualiza e instala dependências básicas
$SUDO apt-get update -y
$SUDO apt-get install -y wget gnupg unzip curl libnss3 libxss1 libasound2 fonts-liberation xdg-utils --no-install-recommends

# 2. Instala Google Chrome
if ! command -v google-chrome &> /dev/null; then
    echo "🌐 Instalando Google Chrome..."
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | $SUDO apt-key add -
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | $SUDO tee /etc/apt/sources.list.d/google-chrome.list
    $SUDO apt-get update -y
    $SUDO apt-get install -y google-chrome-stable --no-install-recommends
fi

# 3. Limpeza
$SUDO rm -rf /var/lib/apt/lists/*

# 4. Dependências Python (Usando o caminho da Action)
echo "🐍 Instalando dependências Python..."
pip install --upgrade pip

# IMPORTANTE: Procurar o requirements.txt na pasta onde a Action foi baixada
if [ -f "$ACTION_PATH/requirements.txt" ]; then
    pip install -r "$ACTION_PATH/requirements.txt"
    echo "✅ requirements.txt instalado."
else
    echo "⚠️ requirements.txt não encontrado em $ACTION_PATH, instalando Selenium manualmente."
    pip install --upgrade selenium pygithub
fi

# 5. Execução do Bot
echo "🤖 Iniciando o bot Alura..."
# Executa o main.py que está na pasta da Action
python "$ACTION_PATH/main.py"