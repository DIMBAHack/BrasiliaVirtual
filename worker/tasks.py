# worker/tasks.py

import logging
import time
from celery import shared_task, Task
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

from worker.celery_app import celery_app


# ════════════════════════════════════════════════════
# TASK 1 — Processar chunk
# ════════════════════════════════════════════════════

@celery_app.task(
    bind=True,
    name="worker.tasks.process_chunk",
    queue="chunks",

    # ── Rate limiting ──────────────────────────────
    # "10/m" = no máximo 10 execuções por minuto por worker
    # Ajuste conforme o limite da sua API externa
    rate_limit="50/m",

    # ── Retry com backoff exponencial ─────────────
    # Se a API externa retornar 429 (rate limit) ou erro,
    # aguarda 2^retry * 10s antes de tentar de novo:
    # tentativa 1 → 10s, tentativa 2 → 20s, tentativa 3 → 40s
    max_retries=5,
    default_retry_delay=10,

    # ── Confiabilidade ────────────────────────────
    acks_late=True,               # confirma só após processar (não perde task se worker cair)
    reject_on_worker_lost=True,   # recoloca na fila se o processo morrer no meio
)
def process_chunk(self, doc_id: str, index: int, text: str):
    try:
        # ── Análise (chama as APIs externas) ────────
        # ── Salva resultado no MongoDB ───────────────
        # retorna resultado para o chord saber que terminou
        # return {"doc_id": doc_id, "index": index, "label": label}
        pass

    except Exception as exc:
        # API externa retornou 429 — backoff exponencial
        retry_in = 10 * (2 ** self.request.retries)
        raise self.retry(exc=exc, countdown=retry_in)

    except Exception as exc:
        raise self.retry(exc=exc)


# ════════════════════════════════════════════════════
# TASK 2 — Finalizar documento (callback do chord)
# ════════════════════════════════════════════════════

@celery_app.task(
    name="worker.tasks.finalize_document",
    queue="finalize",
    max_retries=3,
    default_retry_delay=5,
)
def finalize_document(results: list[dict], doc_id: str):
    """
    Chamada automaticamente pelo chord quando TODOS os chunks terminarem.
    'results' é a lista de retornos de cada process_chunk.
    """

    db = get_db() # pegar o banco
    db["documents"].update_one(
        {"_id": ObjectId(doc_id)},
        {"$set": {
            "status":       "completed",
            "completed_at": datetime.utcnow(),
        }}
    )