import streamlit as st
import pandas as pd
from pymongo import MongoClient
import requests

# Configurando conexão com o MongoDB
client = MongoClient(
    'mongodb://teste:teste@localhost:27017/admin')
db = client['teste']

# Coletando dados de estoque e mix de produtos
estoque = db['ESTOQUE']
mix_produto = db['MIX_PRODUTO']
produto_ean = db['PRODUTO_EAN']

# Convertendo para DataFrame para facilitar a manipulação
df_estoque = pd.DataFrame(list(estoque.find({})))
df_mix_produto = pd.DataFrame(list(mix_produto.find({})))
df_produto_ean = pd.DataFrame(list(produto_ean.find({})))

# Filtrando os 20 primeiros de cada DataFrame
df_estoque = df_estoque.head(5)
df_mix_produto = df_mix_produto.head(5)
df_produto_ean = df_produto_ean.head(5)

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
Com base nos dados de estoque e mix de produto, forneça uma otimização do meu mix de produto
Vou te explicar o que é cada campo para te ajudar nesta análise 
vou começar pelo estoque:

id_empresa (String): Identificação única da empresa, representada por um código.
id_filial_loja_empresa (Int32): Identificação numérica da filial específica da empresa onde os produtos estão armazenados.
ean_produto (String): Código EAN (European Article Number) do produto. É um identificador global exclusivo para o item em questão.
codigo_produto_cliente (Int32): Código interno do produto usado pelo cliente.
tipo_local_estoque (String): Tipo de local onde o estoque está armazenado.
local_estoque (String): Local específico de armazenamento do produto.
saldo_atual (Int32): Quantidade atual do estoque disponível para esse produto.
custo_atual (Int32): Valor do custo atual associado ao produto no estoque.
estoque_padrao (Double): Nível de estoque padrão ou esperado para o produto.
id_cliente_agent (String): Identificador único do cliente/agente responsável ou associado ao produto.
id_filial_loja (String): Identificação da loja ou filial relacionada ao produto em questão.
nome_agente (String): Nome do agente ou responsável vinculado a este estoque ou processo.
status_process (String): ignore este campo.
data_process_agent (String): ignore este campo.
collection_control (String): Informação que indica a origem ou controle do dado, neste caso representando "ESTOQUE".
data_to_load (String): ignora este campo.

Agora vamos para mix_produto:
cnpj (String): Número do Cadastro Nacional da Pessoa Jurídica, identificador fiscal da empresa no Brasil.
ean (String): Código EAN (European Article Number) que identifica o produto de maneira única em nível global.
linha (String): Combinação de diferentes informações sobre o produto separadas por um delimitador, incluindo CNPJ, EAN, código de produto, nome e detalhes adicionais.
id_cliente_agent (String): Identificador único do agente ou cliente associado ao mix de produtos.
id_empresa (String): Código identificador da empresa para vincular as informações ao sistema da empresa responsável.
id_filial_loja (String): Identificação da filial ou loja relacionada ao mix de produtos.
nome_agente (String): Nome do agente responsável por gerenciar ou realizar processos relacionados a este mix de produtos.
status_process (String): ignore este campo
data_process_agent (String): ignore este campo
collection_control (String): Tipo de coleção de dados que está sendo controlada indicando que essas informações estão relacionadas ao mix de produtos.
data_to_load (String): ignore este campo
Por favor, responda em português.
Estoque: {df_estoque.to_dict()}
Mix de Produto: {df_mix_produto.to_dict()} 
"""


# Função para executar a análise do Ollama
def gerar_analise():
    response = requests.post(url='http://localhost:11434/api/generate',
                             json={
                                 "prompt": prompt,
                                 "model": "phi3",
                                 "options": {
                                     "num_ctx": 2048,
                                     "temperature": 0,
                                     "seeds": 150
                                 }
                             }
                             )
    return response.json()


# Botão para gerar a análise
if st.button("Gerar Análise"):
    with st.spinner("Gerando a análise preditiva..."):
        resultado = gerar_analise()
        st.success("Análise concluída!")
        st.write(resultado.get("response"))
