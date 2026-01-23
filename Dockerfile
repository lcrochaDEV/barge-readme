FROM python:3.10-slim

WORKDIR /app
COPY . .

# Dá permissão de execução e roda o script de setup
RUN chmod +x setup.sh && ./setup.sh

CMD ["python", "seu_script.py"]