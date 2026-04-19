# DIMBA — Detector de Integridade Acadêmica v2.0

Analisa trabalhos acadêmicos detectando: **IA generativa**, **plágio**, **fake news** ou **conteúdo autoral**. Construído com FastAPI + MongoDB + Claude/GPT/Gemini.

---

## Estrutura do Projeto

```
AnaliseIA/
├── main.py                        # Entrypoint FastAPI (lifespan unificado)
├── core/
│   ├── config.py                  # Settings via pydantic-settings + .env
│   └── database.py                # Motor (async) + PyMongo (sync) unificados
├── models/
│   ├── db_models.py               # Pydantic models para MongoDB
│   ├── schemas.py                 # Schemas de request/response da API
│   ├── user_model.py              # Modelos de usuário
│   ├── user_repository.py         # CRUD usuários + integração filesDB
│   └── user_router.py             # Endpoints /users e /users/{id}/files
├── services/
│   ├── agents_service.py          # Instâncias Claude, GPT, Gemini
│   ├── reader_service.py          # Extração de texto (.txt, .pdf, .docx)
│   ├── chunk_service.py           # Segmentação por RecursiveTextSplitter
│   ├── ia_service.py              # Motor de análise (DMBAnalyzer)
│   └── documento_service.py       # Orquestrador upload→análise→MongoDB
├── api/
│   └── rotas_documento.py         # Endpoints /upload/ e /documento/{id}
└── .env                           # Chaves de API e URLs

frontend/
└── index.html                     # Frontend completo de testes (HTML puro)

requirements.txt
```

---

## Configuração

### 1. Copiar o `.env`
```env
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-proj-...
GOOGLE_API_KEY=AIza...
MONGODB_URL=mongodb+srv://usuario:senha@cluster.mongodb.net/
MONGODB_DB_NAME=DMBAI
```

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Iniciar servidor
```bash
uvicorn main:app --reload --port 8000
```

### 4. Abrir o frontend
Abra `frontend/index.html` no navegador (sem servidor necessário).

---

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/upload/` | Envia arquivo + tema → retorna `documento_id` |
| `GET`  | `/documento/{id}` | Consulta status e resultado da análise |
| `POST` | `/users/` | Registra usuário no **usersDB** |
| `GET`  | `/users/{id}/files` | Lista arquivos do usuário no **filesDB** |
| `POST` | `/users/{id}/files` | Salva arquivo vinculado ao usuário |

Documentação interativa: `http://localhost:8000/docs`

---

## Fluxo de Análise

```
Upload (arquivo + tema)
    ↓
Extração de texto (txt/pdf/docx)
    ↓
Chunking (RecursiveTextSplitter, 1500 chars)
    ↓
[BG] Geração de prompts → Claude
    ↓
[BG] Simulação de respostas → Claude + GPT + Gemini
    ↓
[BG] Para cada chunk:
    ├── Perplexidade GPT-2 (< 40 = IA)
    ├── Similaridade TF-IDF + SequenceMatcher vs respostas IA
    ├── Busca web DuckDuckGo (plágio)
    └── Verificação de fatos → Claude (fake news)
    ↓
[BG] Se IA detectada → Dicas pedagógicas → Claude
    ↓
Salva resultado no MongoDB (DMBAI.documentos)
    ↓
Polling do frontend até status = 'concluido'
```

---

## Bugs Corrigidos vs Versão Original

| Arquivo | Problema | Solução |
|---------|----------|---------|
| `main.py` | Dois `app = FastAPI()` no mesmo arquivo | Unificado em um único app com lifespan |
| `configDB.py` | `comman('ping')` (typo), `analiseDB()` inexistente, `datetime.now41()` | Removido, centralizado em `database.py` |
| `ia_service.py` | `self.leitor = ReaderService.get_file_content()` (método errado), `self.segmentador = ChunkService.buscar_chunks()` (instanciação errada), `AgentsService` usada como instância em vez de factory | Corrigidos para chamadas corretas |
| `reader_service.py` | `FastAPI()` dentro de uma classe de serviço, rotas misturadas com lógica | Separado em serviço puro sem FastAPI |
| `agents_service.py` | Atributos de classe recebendo instâncias de métodos | Convertido para métodos estáticos factories |
| `chunk_service.py` | Dependência de Redis sem configuração, métodos sem `self` | Redis removido, memória usada |
| `user_router.py` | Import circular (`from userRouter import get_users_collection`) | Corrigido para `from core.database import MongoDB` |
| Geral | Imports relativos quebrados entre módulos | Padronizados para imports absolutos |
