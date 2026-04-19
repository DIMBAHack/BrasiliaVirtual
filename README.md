# 🎓 DMB AI — Detector de Integridade Acadêmica v2.0

Projeto desenvolvido pela equipe **DIMBA** para o Hackaton do Brasília Virtual, realizado entre os dias 15 e 19 de abril .

---

## 📂 Estrutura do Projeto

O sistema é construído com **FastAPI**, **MongoDB** e **Pydantic**, seguindo uma arquitetura modular:

```text
AnaliseIA/
├── main.py                # Entrypoint FastAPI (lifespan unificado)
├── core/
│   ├── config.py          # Settings via pydantic-settings + .env
│   └── database.py        # Motor (async) + PyMongo (sync) unificados
├── models/
│   ├── db_models.py       # Pydantic models para MongoDB
│   ├── schemas.py         # Schemas de request/response da API
│   ├── user_model.py      # Modelos de usuário
│   ├── user_repository.py # CRUD usuários + integração filesDB
│   └── user_router.py     # Endpoints /users e /users/{id}/files
├── services/
│   ├── agents_service.py  # Instâncias Claude, GPT, Gemini
│   ├── reader_service.py  # Extração de texto (.txt, .pdf, .docx)
│   ├── chunk_service.py   # Segmentação por RecursiveTextSplitter
│   ├── ia_service.py      # Motor de análise (DMBAnalyzer)
│   └── documento_service.py # Orquestrador upload → análise → MongoDB
├── api/
│   └── rotas_documento.py # Endpoints /upload/ e /documento/{id}
└── .env                   # Chaves de API e URLs

frontend/
└── index.html             # Frontend completo de testes (HTML puro)

## ⚙️ Configuração do Ambiente

### 1. Variáveis de Ambiente (.env)
Crie um arquivo `.env` na raiz do projeto e configure as chaves de API e acesso ao banco de dados:
```env
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-proj-...
GOOGLE_API_KEY=AIza...
MONGODB_URL=mongodb+srv://usuario:senha@cluster.mongodb.net/
MONGODB_DB_NAME=DMBAI

# Instalar as dependências necessárias
pip install -r requirements.txt

# Iniciar o servidor via Uvicorn
uvicorn main:app --reload --port 8000

## 🔄 Fluxo de Análise (Pipeline Técnico)

O processamento do **DIMBA** é executado de forma assíncrona para garantir que a API permaneça responsiva enquanto o motor de inteligência processa o conteúdo.

### 1. Ingestão e Preparação
* **Upload:** O arquivo (.pdf, .docx ou .txt) é recebido junto com o tema proposto.
* **Extração:** O `ReaderService` extrai o texto bruto, removendo formatações desnecessárias.
* **Chunking:** O `RecursiveTextSplitter` segmenta o texto em blocos de **1500 caracteres**, garantindo que o contexto seja preservado para a análise dos LLMs.

### 2. Simulação Multi-Agente [Background]
Antes da verificação final, o sistema prepara uma base de comparação:
* **Geração de Referência:** O Claude gera prompts baseados no tema do trabalho.
* **Simulação Cross-Model:** O sistema solicita respostas para esses prompts ao **Claude, GPT e Gemini**, criando um "DNA" de como as IAs escreveriam sobre aquele assunto específico.

### 3. Motor de Verificação (DMBAnalyzer)
Para cada bloco (chunk) de texto, são aplicadas quatro camadas de detecção:

| Camada | Método | Critério de Alerta |
| :--- | :--- | :--- |
| **Probabilidade IA** | Perplexidade GPT-2 | Score **< 40** indica alta previsibilidade (padrão de máquina). |
| **Similaridade** | TF-IDF + SequenceMatcher | Comparação direta com as respostas simuladas dos modelos Claude/GPT/Gemini. |
| **Plágio** | DuckDuckGo Search | Busca por trechos exatos ou paráfrases em fontes da web. |
| **Integridade de Fatos** | Fact-Checking (Claude) | Identificação de "alucinações" ou informações inventadas (Fake News). |

### 4. Inteligência Pedagógica
* **Diagnóstico:** Se a probabilidade de IA ultrapassar o threshold de **75%**, o sistema não apenas sinaliza, mas analisa o *estilo* da escrita.
* **Feedback:** O Claude gera dicas pedagógicas personalizadas, orientando o aluno sobre como tornar o texto mais autoral e profundo.

### 5. Finalização e Persistência
* **Armazenamento:** O relatório completo (scores, links de plágio e vereditos) é salvo no **MongoDB** (coleção `DMBAI.documentos`).
* **Notificação:** O status do documento é alterado para `concluido`, liberando o resultado para o polling do frontend.
