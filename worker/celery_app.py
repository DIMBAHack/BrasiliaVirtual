from celery import Celery
from core.config import settings

# ──────────────────────────────────────────
# Instância do Celery
# ──────────────────────────────────────────
# broker  → Redis recebe as tasks enfileiradas pela API
# backend → Redis armazena o estado/resultado das tasks
# ──────────────────────────────────────────

celery_app = Celery(
    "plagiarism_checker",
    broker  = settings.REDIS_URL,
    backend = settings.REDIS_URL,
)

celery_app.conf.update(
    # Serialização
    task_serializer   = "json",
    result_serializer = "json",
    accept_content    = ["json"],

    # Filas
    task_default_queue = "chunks",          # fila padrão para chunks
    task_queues        = {                  # filas adicionais
        "chunks":   {"exchange": "chunks"},
        "finalize": {"exchange": "finalize"},
    },

    # Retry automático em caso de falha
    task_acks_late              = True,     # confirma só após processar
    task_reject_on_worker_lost  = True,     # recoloca na fila se worker cair
    worker_prefetch_multiplier  = 1,        # 1 task por vez por worker

    # Resultados
    result_expires = 60 * 60 * 24,         # mantém resultados por 24h

    # Timezone
    timezone       = "America/Sao_Paulo",
    enable_utc     = True,
)

# Autodiscover registra automaticamente tasks em worker/tasks.py
celery_app.autodiscover_tasks(["worker"])