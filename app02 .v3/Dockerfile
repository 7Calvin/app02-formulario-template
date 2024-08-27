# Base image
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo requirements.txt e instala as dependências
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia o conteúdo do diretório atual para o diretório de trabalho no container
COPY . .

# Expõe a porta que o Flask irá rodar
EXPOSE 5000

# Comando para rodar o aplicativo Flask
CMD ["python", "app.py"]
