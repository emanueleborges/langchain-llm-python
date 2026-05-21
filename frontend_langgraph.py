import streamlit as st
import os
import asyncio
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Literal, TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnableConfig

# Configuração da página
st.set_page_config(
    page_title="🗺️ Roteador de Viagem",
    page_icon="🧭",
    layout="centered"
)

st.title("🗺️ Roteador Inteligente de Viagem")
st.markdown("Descreva o que procura e seja roteado para o especialista certo!")

# Carregar variáveis de ambiente
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("❌ Chave de API não configurada. Verifique seu arquivo .env")
    st.stop()

# Definir modelo
modelo = ChatOpenAI(
    model="deepseek-chat",
    temperature=0.5,
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# Prompts dos consultores
prompt_consultor_praia = ChatPromptTemplate.from_messages(
    [
        ("system", "Apresente-se como Sra Praia. Você é uma especialista em viagens com destinos para praia. Seja entusiasta e forneça recomendações específicas."),
        ("human", "{query}")
    ]
)

prompt_consultor_montanha = ChatPromptTemplate.from_messages(
    [
        ("system", "Apresente-se como Sr Montanha. Você é um especialista em viagens com destinos para montanhas e atividades radicais. Seja entusiasta e forneça recomendações emocionantes."),
        ("human", "{query}")
    ]
)

# Cadeias dos consultores
cadeia_praia = prompt_consultor_praia | modelo | StrOutputParser()
cadeia_montanha = prompt_consultor_montanha | modelo | StrOutputParser()

# Prompt do roteador
prompt_roteador = ChatPromptTemplate.from_messages(
    [
        ("system", "Você é um roteador. Responda APENAS com a palavra 'praia' ou 'montanha', sem nenhum texto adicional."),
        ("human", "{query}")
    ]
)

# Parseador personalizado
def parseador_rota(texto: str):
    texto_limpo = texto.strip().lower()
    if "praia" in texto_limpo:
        return {"destino": "praia"}
    else:
        return {"destino": "montanha"}

# Roteador
roteador = prompt_roteador | modelo | StrOutputParser() | parseador_rota

# TypedDict para o estado
class Rota(TypedDict):
    destino: Literal["praia", "montanha"]

class Estado(TypedDict):
    query: str
    destino: Rota
    resposta: str

# Funções dos nós do grafo
async def no_roteador(estado: Estado, config=RunnableConfig):
    return {"destino": await roteador.ainvoke({"query": estado["query"]}, config)}

async def no_praia(estado: Estado, config=RunnableConfig):
    return {"resposta": await cadeia_praia.ainvoke({"query": estado["query"]}, config)}

async def no_montanha(estado: Estado, config=RunnableConfig):
    return {"resposta": await cadeia_montanha.ainvoke({"query": estado["query"]}, config)}

def escolher_no(estado: Estado) -> Literal["praia", "montanha"]:
    return "praia" if estado["destino"]["destino"] == "praia" else "montanha"

# Construir grafo
grafo = StateGraph(Estado)
grafo.add_node("rotear", no_roteador)
grafo.add_node("praia", no_praia)
grafo.add_node("montanha", no_montanha)

grafo.add_edge(START, "rotear")
grafo.add_conditional_edges("rotear", escolher_no)
grafo.add_edge("praia", END)
grafo.add_edge("montanha", END)

app = grafo.compile()

# Interface Streamlit
st.markdown("### 📍 Descreva o que você procura:")

col1, col2 = st.columns([3, 1])

with col1:
    consulta = st.text_input(
        "Sua consulta:",
        placeholder="Ex: Quero escalar montanhas ou visitar praias paradisíacas",
        key="consulta_langgraph"
    )

with col2:
    botao_rotear = st.button("🧭 Rotear", use_container_width=True)

if botao_rotear and consulta.strip():
    with st.spinner("🤖 Roteando sua consulta..."):
        try:
            # Executar grafo assincronamente
            async def executar_grafo():
                resultado = await app.ainvoke({"query": consulta})
                return resultado
            
            # Executar loop de eventos
            resultado = asyncio.run(executar_grafo())
            
            # Exibir resultado
            st.success("✅ Roteamento concluído!")
            
            st.markdown("---")
            
            # Mostrar qual especialista atendeu
            tipo_viagem = resultado["destino"]["destino"]
            if tipo_viagem == "praia":
                st.markdown("### 🏖️ Atendida por: **Sra. Praia**")
                st.info("Especialista em destinos de praia")
            else:
                st.markdown("### ⛰️ Atendida por: **Sr. Montanha**")
                st.info("Especialista em montanhas e atividades radicais")
            
            st.markdown("---")
            st.markdown("### 💬 Recomendação:")
            st.success(resultado["resposta"])
            
        except Exception as e:
            st.error(f"❌ Erro ao processar: {str(e)}")

st.markdown("---")
st.markdown("""
### 🎯 Como Funciona
1. **Entrada**: Você descreve o tipo de viagem desejada
2. **Roteamento**: O sistema identifica se é praia ou montanha
3. **Especialista**: Conecta você com o especialista apropriado
4. **Recomendação**: Recebe uma resposta personalizada

### 👥 Especialistas
- 🏖️ **Sra. Praia**: Praias, litoral, resorts, água
- ⛰️ **Sr. Montanha**: Montanhas, trilhas, radicais, natureza selvagem

### 💡 Exemplos de Entrada
- "Quero relaxar em praias paradisíacas"
- "Procuro aventura em montanhas"
- "Atividades aquáticas"
- "Escalada e trilhas"
""")
