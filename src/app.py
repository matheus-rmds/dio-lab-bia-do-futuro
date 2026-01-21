import json
import pandas as pd
import requests
import streamlit as st

OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss"

perfil = json.load(open('./data/perfil_investidor.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
produtos = json.load(open('./data/produtos_financeiros.json'))

contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_investidor']}.
OBJETIVO: {perfil['objetivo_principal']}.
PATRIMÔNIO: R$ {perfil['patrimonio_total']} | Reserva: R$ {perfil['reserva_emergencia_atual']}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""

SYSTEM_PROMPT = """
Você é o Finon, um educador financeiro amigável e didático.

OBJETIVO:
Ensinar conceitos de finanças pessoais de forma simples, usando os dados do cliente como exemplos práticos.

REGRAS:
1. NUNCA recomendo investimentos específicos, apenas explique como funcionam
2. Use os dados fornecidos para dar exemplos personalizados
3. Linguagem simples, como se estivesse explicando para um amigo
4. Se não souber de algo, admita "Não tenho essa informação, mas posso explicar... "
5. Sempre pergunte se o cliente entendeu a explicação
6. Explique de forma direta e sucinta, com no máximo 3 parágrafos
"""

def perguntar(msg):
    prompt = f"""
    {SYSTEM_PROMPT}

    CONTEXTO DO CLIENTE:
    {contexto}

    PERGUNTA: {msg}
    """

    r = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt, "stream": False})
    return r.json()['response']

st.title("Finon - Educador Financeiro Virtual")
if pergunta := st.chat_input("Sua dúvida sobre finanças pessoais..."):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta))