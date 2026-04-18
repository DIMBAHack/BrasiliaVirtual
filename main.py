from contextlib import asynccontextmanager
from fastapi import FastAPI
from AnaliseIA.core.database import conectar, desconectar
from api.routes import Routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    await conectar()
    yield
    await desconectar()


app = FastAPI(lifespan=lifespan)
app.include_router(Routes)