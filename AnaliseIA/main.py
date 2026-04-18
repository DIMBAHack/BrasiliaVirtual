from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.database import conectar, desconectar
from api.rotas_documento import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await conectar()
    yield
    await desconectar()


app = FastAPI(lifespan=lifespan)
app.include_router(router)

from fastapi import FastAPI
from contextlib import asynccontextmanager

from models.connection import MongoDB
from models.userRouter import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    MongoDB.connect()
    yield
    MongoDB.disconnect()


app = FastAPI(
    title="Users & Files API",
    description="API para gerenciamento de usuários e arquivos com MongoDB",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(user_router)


@app.get("/")
def root():
    return {"status": "online", "docs": "/docs"}