# Usar a imagem oficial do Python
FROM python:3.12

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    python3-pyaudio \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*


# Definir o diretório de trabalho
WORKDIR /code

# Copiar apenas o requirements.txt primeiro
COPY requirements.txt /code/

# Instalar dependências Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar o resto da aplicação
COPY . /code/

# Comando para iniciar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]