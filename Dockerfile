# Imagem base para construir a aplicação FastAPI
FROM python:3.11-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie os arquivos de configuração e código-fonte da aplicação para o diretório de trabalho
COPY . .

# Instale as dependências
RUN pip install poetry==1.1.13
RUN poetry config virtualenvs.create false
RUN poetry install

# Exponha a porta em que a aplicação FastAPI está sendo executada
EXPOSE 8000

# Execute a aplicação FastAPI
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
