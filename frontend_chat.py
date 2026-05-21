import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

# Configuração da página
st.set_page_config(
    page_title="💬 Chat de Viagem",
    page_icon="🗺️",
    layout="centered"
)

st.title("💬 Chat de Viagem com Memória")
st.markdown("Converse com um guia de viagem especializado em destinos brasileiros")

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

# Prompt
prompt_sugestao = ChatPromptTemplate.from_messages(
    [
        ("system", "Você é um guia de viagem especializado em destinos brasileiros. Apresente-se como Sr. Passeios. Responda com entusiasmo e forneça recomendações úteis."),
        ("human", "{query}")
    ]
)

# Parser
parser = StrOutputParser()

# Inicializar histórico na sessão
if "historico_chat" not in st.session_state:
    st.session_state.historico_chat = []

# Cadeia
cadeia = prompt_sugestao | modelo | parser

# Exibir histórico
st.markdown("### 📝 Histórico da Conversa")

for mensagem in st.session_state.historico_chat:
    if mensagem["tipo"] == "usuario":
        st.chat_message("user").write(mensagem["conteudo"])
    else:
        st.chat_message("assistant").write(mensagem["conteudo"])

# Input
st.markdown("---")
pergunta = st.text_input(
    "🤔 Faça sua pergunta:",
    placeholder="Ex: Quero visitar um lugar com praias. Pode sugerir?",
    key="pergunta_input"
)

col1, col2 = st.columns([4, 1])

with col2:
    botao_enviar = st.button("📤 Enviar", use_container_width=True)

if botao_enviar and pergunta.strip():
    # Adicionar pergunta ao histórico
    st.session_state.historico_chat.append({
        "tipo": "usuario",
        "conteudo": pergunta
    })
    
    with st.spinner("🤖 Sr. Passeios está pensando..."):
        try:
            # Invocar cadeia
            resposta = cadeia.invoke({"query": pergunta})
            
            # Adicionar resposta ao histórico
            st.session_state.historico_chat.append({
                "tipo": "assistente",
                "conteudo": resposta
            })
            
            # Recarregar página
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Erro ao processar: {str(e)}")

# Botão para limpar histórico
st.markdown("---")
if st.button("🗑️ Limpar Histórico"):
    st.session_state.historico_chat = []
    st.success("Histórico limpo!")
    st.rerun()

st.markdown("""
---
### 💡 Dicas
- Faça perguntas sobre destinos brasileiros
- Sr. Passeios está aqui para ajudar
- Você pode pedir recomendações específicas
""")

