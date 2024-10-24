# Usar uma imagem base Python
FROM python:3.12-slim as Build

# Instalar as dependências necessárias
WORKDIR /app

# Copiar requirements.txt e instalar dependências
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY . .

# Expor a porta usada pelo Streamlit
EXPOSE 8501

# Comando para rodar o Streamlit
CMD ["streamlit", "run", "main.py"]