import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from pydantic import Field, BaseModel

# Configuração da página
st.set_page_config(
    page_title="🌍 Recomendador de Destinos",
    page_icon="✈️",
    layout="centered"
)

st.title("✈️ Recomendador de Destinos Turísticos")
st.markdown("Descubra cidades incríveis com base em seus interesses usando IA!")

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

# Definir modelos de dados
class Destino(BaseModel):
    cidade: str = Field("A cidade recomendada para visitar")
    motivo: str = Field("motivo pelo qual é interessante visitar essa cidade")

class Restaurantes(BaseModel):
    cidade: str = Field("A cidade recomendada para visitar")
    restaurantes: str = Field("Restaurantes recomendados na cidade")

# Parsers
parseador_destino = JsonOutputParser(pydantic_object=Destino)
parseador_restaurantes = JsonOutputParser(pydantic_object=Restaurantes)

# Prompts
prompt_cidade = PromptTemplate(
    template="""
    Sugira uma cidade dado o meu interesse por {interesse}.
    {formato_de_saida}
    """,
    input_variables=["interesse"],
    partial_variables={"formato_de_saida": parseador_destino.get_format_instructions()}
)

prompt_restaurantes = PromptTemplate(
    template="""
    Sugira restaurantes populares entre locais em {cidade}
    {formato_de_saida}
    """,
    partial_variables={"formato_de_saida": parseador_restaurantes.get_format_instructions()}
)

prompt_cultural = PromptTemplate(
    template="Sugira atividades e locais culturais em {cidade}"
)

# Cadeias
cadeia_1 = prompt_cidade | modelo | parseador_destino
cadeia_2 = prompt_restaurantes | modelo | parseador_restaurantes
cadeia_3 = prompt_cultural | modelo | StrOutputParser()

cadeia = (cadeia_1 | cadeia_2 | cadeia_3)

# Interface
col1, col2 = st.columns([3, 1])

with col1:
    interesse = st.text_input(
        "📍 Qual é seu interesse? (ex: praias, montanhas, história)",
        placeholder="Digite seu interesse..."
    )

with col2:
    botao_buscar = st.button("🔍 Buscar", use_container_width=True)

if botao_buscar:
    if not interesse.strip():
        st.warning("⚠️ Por favor, digite um interesse!")
    else:
        with st.spinner("🤖 Procurando a melhor recomendação..."):
            try:
                resposta = cadeia.invoke({"interesse": interesse})
                
                st.success("✅ Recomendação encontrada!")
                
                st.markdown("---")
                st.markdown("### 🏙️ Destino Recomendado")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Cidade", resposta.get("cidade", "N/A"))
                with col2:
                    st.info(f"**Motivo:** {resposta.get('motivo', 'N/A')}")
                
                st.markdown("---")
                st.markdown("### 🍽️ Restaurantes")
                st.info(resposta.get("restaurantes", "Sem informações"))
                
                st.markdown("---")
                st.markdown("### 🎭 Atividades Culturais")
                st.success(resposta)
                
            except Exception as e:
                st.error(f"❌ Erro ao processar: {str(e)}")

st.markdown("---")
st.markdown("### 💡 Dicas de Interesse")
st.markdown("""
- 🏖️ **Praias** - Cidades costeiras com beleza natural
- 🏔️ **Montanhas** - Destinos para trilhas e ecoturismo
- 🏛️ **História** - Cidades com patrimônio histórico
- 🍴 **Gastronomia** - Destinos culinários
- 🌿 **Natureza** - Ecoturismo e biodiversidade
""")
