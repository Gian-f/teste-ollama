import streamlit as st
import pandas as pd
from pymongo import MongoClient
import requests

# Configurando conexão com o MongoDB
client = MongoClient(
    'mongodb://gian:248e2f74b381cbf17cb3b1566a1b4461c80bc0f43212c73f346df53cc952bef7@192.168.23.42:27017/admin')
db = client['datalake_3_1_5']

# Coletando dados de estoque e mix de produtos
estoque = db['ESTOQUE']
mix_produto = db['MIX_PRODUTO']
produto_ean = db['PRODUTO_EAN']

# Convertendo para DataFrame para facilitar a manipulação
df_estoque = pd.DataFrame(list(estoque.find({})))
df_mix_produto = pd.DataFrame(list(mix_produto.find({})))
df_produto_ean = pd.DataFrame(list(produto_ean.find({})))

# Filtrando os 20 primeiros de cada DataFrame
df_estoque = df_estoque.head(20)
df_mix_produto = df_mix_produto.head(20)
df_produto_ean = df_produto_ean.head(20)

# Exibindo os dados no Streamlit
st.title("Análise de Estoque e Mix de Produtos")
st.write("Estoque")
st.dataframe(df_estoque)

st.write("Mix de Produtos")
st.dataframe(df_mix_produto)

st.write("Produto EAN")
st.dataframe(df_produto_ean)

# Definindo o prompt para análise do Ollama
prompt = f"""
Com base nos dados de estoque e mix de produto, forneça uma análise preditiva para otimizar as campanhas promocionais.
Estoque: {df_estoque.to_dict()}
Mix de Produto: {df_mix_produto.to_dict()}
Produto EAN: {df_produto_ean.to_dict()}
"""


# Função para executar a análise do Ollama
def gerar_analise():
    return requests.post(url='http://localhost:11434/api/generate',
                         json={
                             "prompt": prompt,
                             "stream": False,
                             "model": "phi3",

                         })


# Botão para gerar a análise
if st.button("Gerar Análise"):
    with st.spinner("Gerando a análise preditiva..."):
        resultado = gerar_analise()
        st.success("Análise concluída!")
        st.write(resultado)
