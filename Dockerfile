FROM python:3.10-slim

# Definir diretório de trabalho
WORKDIR /app

# 1. Instalar dependências de rede e sistema (equivalente ao início do seu .sh)
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    --no-install-recommends

# 2. Configurar o repositório do Google Chrome (Exatamente como no seu .sh)
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list

# 3. Instalar Chrome e bibliotecas para modo Headless
RUN apt-get update && apt-get install -y \
    google-chrome-stable \
    libnss3 \
    libxss1 \
    libasound2 \
    fonts-liberation \
    libgbm1 \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# 4. Copiar apenas o requirements primeiro (Otimização de Cache)
COPY requirements.txt .

# 5. Instalar/Atualizar Selenium e dependências do projeto
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Copiar o restante do código
COPY . .

# Comando para iniciar
CMD ["python", "main.py"]