from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.database import conectar, desconectar, MongoDB
from api.rotas_documento import router as doc_router
from models.user_router import router as user_router

# Importe seu router (o código que você me enviou)
# from routers.user_router import router as user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Conecta Motor (async) e PyMongo (sync)
    await conectar()
    MongoDB.connect()
    yield
    await desconectar()
    MongoDB.disconnect()


app = FastAPI(
    title="DIMBA — Detector de Integridade Acadêmica",
    description=(
        "Analisa trabalhos acadêmicos detectando conteúdo gerado por IA, "
        "plágio, fake news ou conteúdo autoral. "
        "Integra gerenciamento de usuários e arquivos via MongoDB."
    ),
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Ajuste para as URLs do seu front-end
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(doc_router)
app.include_router(user_router)
# 1. Configuração de CORS (Obrigatório para o front-end acessar os arquivos)

# 2. Configuração de Arquivos Estáticos (Static Files)
# Isso diz ao FastAPI: "Tudo o que for pedido em /uploads, procure na pasta local 'uploads'"
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")

# 3. Inclusão de Rotas
# app.include_router(user_router)

@app.get("/")
def home():
    return {"mensagem": "API ativa"}

from fastapi import Request
from fastapi.responses import JSONResponse
import traceback

@app.middleware("http")
async def catch_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        traceback.print_exc()  # aparece no terminal
        return JSONResponse(
            status_code=500,
            content={"detail": str(e)},
            headers={"Access-Control-Allow-Origin": "*"},  # evita mascarar como CORS
        )