from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
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

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# 3. Inclusão de Rotas
# app.include_router(user_router)

@app.get("/")
def home():
    return {"mensagem": "API ativa"}