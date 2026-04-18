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