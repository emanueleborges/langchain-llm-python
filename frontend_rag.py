import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Configuração da página
st.set_page_config(
    page_title="📚 Consulta de Documentos",
    page_icon="🔍",
    layout="wide"
)

st.title("📚 Consulta de Documentos com RAG")
st.markdown("Faça perguntas sobre documentos PDF usando busca semântica")

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

# Definir embeddings
@st.cache_resource
def obter_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Carregar documentos em cache
@st.cache_resource
def carregar_documentos():
    arquivos = [
        "documentos/GTB_gold_Nov23.txt"
    ]
    
    documentos = []
    for arquivo in arquivos:
        if os.path.exists(arquivo):
            try:
                with open(arquivo, 'r', encoding='utf-8') as f:
                    conteudo = f.read()
                    documentos.append({
                        "page_content": conteudo,
                        "metadata": {"source": arquivo}
                    })
                st.success(f"✅ Documento carregado: {arquivo}")
            except Exception as e:
                st.warning(f"⚠️ Erro ao carregar {arquivo}: {e}")
    
    if not documentos:
        st.error("❌ Nenhum documento encontrado na pasta 'documentos/'")
        return None
    
    # Split documentos
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    
    pedacos = []
    for doc in documentos:
        chunks = splitter.split_text(doc["page_content"])
        pedacos.extend(chunks)
    
    embeddings = obter_embeddings()
    vectorstore = FAISS.from_texts(pedacos, embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 3})

# Carregar dados
st.info("📂 Carregando documentos...")
retriever = carregar_documentos()

if retriever is None:
    st.stop()

# Prompt
prompt_consulta = ChatPromptTemplate.from_messages(
    [
        ("system", "Você é um assistente que responde perguntas usando APENAS o conteúdo fornecido. Se a resposta não está no contexto, diga que não sabe."),
        ("human", "{query}\n\nContexto dos documentos:\n{contexto}\n\nResposta:")
    ]
)

# Parser
parser = StrOutputParser()

# Cadeia
cadeia = prompt_consulta | modelo | parser

# Interface
st.markdown("---")
st.markdown("### 🔍 Faça sua Pergunta")

col1, col2 = st.columns([4, 1])

with col1:
    pergunta = st.text_input(
        "❓ Sua pergunta sobre os documentos:",
        placeholder="Ex: Como proceder em caso de roubo com cartão platinum?",
        key="pergunta_rag"
    )

with col2:
    botao_buscar = st.button("🔎 Buscar", use_container_width=True)

if botao_buscar and pergunta.strip():
    with st.spinner("🤖 Procurando nos documentos..."):
        try:
            # Recuperar trechos relevantes
            trechos = retriever.invoke(pergunta)
            
            # Extrair page_content dos documentos
            trechos_texto = [trecho.page_content if hasattr(trecho, 'page_content') else str(trecho) for trecho in trechos]
            
            # Construir contexto
            contexto = "\n\n---\n\n".join(
                f"📄 {i+1}. {texto[:500]}..." 
                for i, texto in enumerate(trechos_texto)
            )
            
            # Gerar resposta
            resposta = cadeia.invoke({
                "query": pergunta,
                "contexto": contexto
            })
            
            st.success("✅ Resposta gerada!")
            
            st.markdown("---")
            st.markdown("### 💬 Resposta")
            st.info(resposta)
            
            st.markdown("---")
            st.markdown("### 📌 Trechos Relevantes")
            for i, texto in enumerate(trechos_texto):
                with st.expander(f"Trecho {i+1}"):
                    st.text(texto[:1000] + "...")
            
        except Exception as e:
            st.error(f"❌ Erro ao processar: {str(e)}")

st.markdown("---")
st.markdown("""
### 💡 Como Funciona
1. **RAG (Retrieval-Augmented Generation)**: Busca trechos relevantes nos documentos
2. **Embeddings**: Usa similaridade semântica para encontrar informações
3. **Resposta Contextual**: Gera respostas baseadas APENAS nos documentos
4. **Rastreabilidade**: Mostra os trechos usados na resposta

### 📋 Documentos Disponíveis
- GTB_gold_Nov23.txt - Informações sobre cartões Gold
""")
