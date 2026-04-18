
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.database import conectar, desconectar, MongoDB
from api.rotas_documento import router as doc_router
from models.user_router import router as user_router


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

# CORS liberado para o frontend de testes
app.add_middleware(
    CORSMiddleware,
    allow_origins=None,  # Em produção, substitua pelo domínio real
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(doc_router)
app.include_router(user_router)


@app.get("/", tags=["Health"])
def root():
    return {
        "status": "online",
        "versao": "2.0.0",
        "docs": "/docs",
        "endpoints": {
            "upload_analise": "POST /upload/",
            "buscar_resultado": "GET /documento/{id}",
            "usuarios": "/users",
        },
    }
