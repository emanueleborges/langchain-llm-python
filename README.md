<img width="989" alt="image" src="https://github.com/user-attachments/assets/c140d5f9-a165-44d0-80b9-592fdbf16e03" />

# LangChain e Python: criando ferramentas com LLM Deepseek

Projeto educacional da Alura para integração de modelos de linguagem usando LangChain e Python com a API Deepseek.

## ⚙️ Guia de Configuração

Siga os passos abaixo para configurar seu ambiente e utilizar os scripts do projeto.

### 1. Criar e Ativar Ambiente Virtual

**Windows:**

```bash
python -m venv langchain
langchain\Scripts\activate
```

**Mac/Linux:**

```bash
python3 -m venv langchain
source langchain/bin/activate
```

### 2. Instalar Dependências

Utilize o comando abaixo para instalar as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

### 3. Configurar Chave da Deepseek API

Crie ou edite o arquivo `.env` adicionando sua chave de API da Deepseek:

```env
OPENAI_API_KEY=sk-your-deepseek-api-key-here
```

**Como obter sua chave Deepseek:**
1. Acesse [https://platform.deepseek.com](https://platform.deepseek.com)
2. Crie uma conta ou faça login
3. Navegue até a seção de API keys
4. Copie sua chave e adicione ao arquivo `.env`

## 🚀 Executando o Projeto

Para executar o script principal que utiliza o Deepseek para sugerir destinos turísticos:

```bash
python main.py
```

### 🎨 Interfaces Web (Streamlit)

Também existem frontends interativos para cada aplicação. Instale Streamlit (se ainda não tiver):

```bash
pip install streamlit
```

Depois execute qualquer uma das interfaces:

**1. Recomendador de Destinos:**
```bash
streamlit run frontend_main.py
```

**2. Chat de Viagem com Memória:**
```bash
streamlit run frontend_chat.py
```

**3. Consulta de Documentos (RAG):**
```bash
streamlit run frontend_rag.py
```

**4. Roteador Inteligente de Viagem:**
```bash
streamlit run frontend_langgraph.py
```

Cada interface abrirá em `http://localhost:8501`

### Scripts Disponíveis

- **main.py** - Script principal com cadeia completa de recomendações
- **main_chat.py** - Interface de chat com Deepseek
- **main_rag.py** - Implementação de RAG (Retrieval-Augmented Generation)
- **main_langgraph.py** - Usando LangGraph para fluxos complexos

### 🎨 Interfaces Web (Streamlit)

| Interface | Comando | Descrição |
|-----------|---------|-----------|
| **Recomendador** | `streamlit run frontend_main.py` | 🏖️ Recomenda destinos com restaurantes e atividades culturais |
| **Chat** | `streamlit run frontend_chat.py` | 💬 Conversa com Sr. Passeios mantendo histórico |
| **RAG** | `streamlit run frontend_rag.py` | 📚 Consulta documentos com busca semântica |
| **Roteador** | `streamlit run frontend_langgraph.py` | 🧭 Roteia para especialista (praia ou montanha) |

## 📋 Estrutura do Projeto

```
.
├── main.py                   # Script principal
├── main_chat.py              # Chat interativo
├── main_rag.py               # RAG com documentos
├── main_langgraph.py         # LangGraph workflows
│
├── frontend_main.py          # 🎨 Interface Streamlit - Recomendador
├── frontend_chat.py          # 🎨 Interface Streamlit - Chat
├── frontend_rag.py           # 🎨 Interface Streamlit - RAG
├── frontend_langgraph.py     # 🎨 Interface Streamlit - Roteador
│
├── requirements.txt          # Dependências
├── .env                      # Variáveis de ambiente
├── README.md                 # Este arquivo
└── documentos/               # Documentos para RAG
    └── GTB_gold_Nov23.txt
```

## 🔧 Configuração Técnica

- **Modelo**: deepseek-chat
- **Base URL**: https://api.deepseek.com
- **Framework**: LangChain
- **Parser**: JsonOutputParser para saídas estruturadas
- **Temperatura**: 0.5 (respostas balanceadas)

## ⚠️ Troubleshooting

**Erro: "python-dotenv could not parse statement"**
- Verifique se o arquivo `.env` está bem formatado (sem caracteres especiais ou aspas desalinhadas)

**Erro: "Insufficient quota"**
- Verifique sua chave de API no [painel Deepseek](https://platform.deepseek.com)
- Confirme se sua conta tem créditos disponíveis

**Erro: "Module not found"**
- Execute `pip install -r requirements.txt` novamente
- Se o problema persistir, reative o ambiente virtual e tente novamente

## 📚 Recursos

- [Documentação LangChain](https://python.langchain.com/)
- [API Deepseek](https://platform.deepseek.com)
- [Curso Alura](https://www.alura.com.br)
