"""
FastAPI App Main Entry Point
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI

# Import routers
from api.rotas_documento import router as doc_router
from api.rotas_webhooks import router as webhook_router
from models.userRouter import router as user_router

# Import database connections
try:
    from models.connection import MongoDB
    use_motor = True
except ImportError:
    use_motor = False

try:
    from core.database import conectar, desconectar
except ImportError:
    conectar = None
    desconectar = None


# ─── LIFESPAN CONTEXT ───
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    try:
        if use_motor and hasattr(MongoDB, 'connect'):
            MongoDB.connect()
        elif conectar:
            await conectar()
    except Exception as e:
        print(f"⚠️  Warning during startup: {e}")
    
    yield
    
    try:
        if use_motor and hasattr(MongoDB, 'disconnect'):
            MongoDB.disconnect()
        elif desconectar:
            await desconectar()
    except Exception as e:
        print(f"⚠️  Warning during shutdown: {e}")


# ─── CREATE APP ───
app = FastAPI(
    title="BrasiliaVirtual API",
    description="API para análise de documentos com detecção de IA, plágio e fake news",
    version="1.0.0",
    lifespan=lifespan,
)

# ─── INCLUDE ROUTERS ───
app.include_router(doc_router)
app.include_router(user_router)
app.include_router(webhook_router)

# ─── ROOT ENDPOINT ───
@app.get("/")
def root():
    return {
        "status": "online",
        "docs": "/docs",
        "service": "BrasiliaVirtual API",
        "version": "1.0.0"
    }


# ─── HEALTH CHECK ───
@app.get("/health")
def health():
    return {"status": "healthy"}