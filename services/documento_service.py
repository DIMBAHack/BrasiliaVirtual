"""
Orquestra upload → chunking → análise → persistência no MongoDB.
"""
import asyncio
from datetime import datetime
from dataclasses import asdict

from bson import ObjectId
from fastapi import UploadFile, HTTPException

from services.reader_service import ReaderService
from services.chunk_service import ChunkService
from services.ia_service import DMBAnalyzer, TrechoAnalise
from core.database import get_async_db


def _trecho_to_dict(t: TrechoAnalise) -> dict:
    return {
        "chunk_number": 0,          # será atualizado no loop
        "text": t.texto,
        "classificacao": t.classificacao,
        "confianca": t.confianca,
        "evidencias": t.evidencias,
        "detalhes": t.detalhes,
    }


class DocumentoService:

    async def processar(self, file: UploadFile, tema: str) -> dict:
        """Lê, chunka, analisa e salva. Retorna documento_id e resumo."""
        db = get_async_db()

        # 1. Extrair texto
        try:
            texto = await ReaderService.extrair_texto(file)
        except ValueError as e:
            raise HTTPException(422, detail=str(e))

        if not texto.strip():
            raise HTTPException(422, detail="O arquivo não contém texto legível.")

        # 2. Dividir em chunks
        chunks = ChunkService.dividir(texto)
        if not chunks:
            raise HTTPException(422, detail="Texto muito curto para análise.")

        # 3. Criar registro no MongoDB com status "processando"
        doc_inicial = {
            "filename": file.filename,
            "tema": tema,
            "status": "processando",
            "total_chunks": len(chunks),
            "criado_em": datetime.utcnow(),
            "concluido_em": None,
            "resultado": None,
            "resumo": None,
            "dicas_ia": None,
        }
        result = await db["documentos"].insert_one(doc_inicial)
        documento_id = str(result.inserted_id)

        # 4. Analisar em background (não bloqueia a resposta HTTP)
        asyncio.create_task(self._analisar_bg(documento_id, chunks, tema, file.filename, db))

        return {
            "documento_id": documento_id,
            "filename": file.filename,
            "tema": tema,
            "total_chunks": len(chunks),
            "status": "processando",
        }

    async def _analisar_bg(self, documento_id: str, chunks, tema, filename, db):
        """Roda a análise pesada em background e atualiza o MongoDB."""
        mensagens = []

        def cb(msg):
            mensagens.append(msg)
            print(f"[BG {documento_id[:8]}] {msg}")

        try:
            analisador = DMBAnalyzer(callback_status=cb)

            # Roda análise em thread para não bloquear event loop
            loop = asyncio.get_event_loop()
            resultado = await loop.run_in_executor(
                None, analisador.analisar, chunks, tema
            )

            # Monta lista de resultados
            todos = []
            for i, t in enumerate(resultado.trechos_ia + resultado.trechos_plagio +
                                  resultado.trechos_fake_news + resultado.trechos_autorais):
                d = _trecho_to_dict(t)
                d["chunk_number"] = i
                todos.append(d)

            total = len(chunks) or 1
            resumo = {
                "total_trechos": len(chunks),
                "trechos_ia": len(resultado.trechos_ia),
                "trechos_plagio": len(resultado.trechos_plagio),
                "trechos_fake_news": len(resultado.trechos_fake_news),
                "trechos_autorais": len(resultado.trechos_autorais),
                "pct_ia": round(len(resultado.trechos_ia) / total * 100, 1),
                "pct_plagio": round(len(resultado.trechos_plagio) / total * 100, 1),
                "pct_fake_news": round(len(resultado.trechos_fake_news) / total * 100, 1),
                "pct_autoral": round(len(resultado.trechos_autorais) / total * 100, 1),
                "perplexidade_media": round(resultado.perplexidade_media, 2),
                "veredicto": _veredicto(resultado),
            }

            await db["documentos"].update_one(
                {"_id": ObjectId(documento_id)},
                {"$set": {
                    "status": "concluido",
                    "concluido_em": datetime.now(),
                    "resultado": todos,
                    "resumo": resumo,
                    "dicas_ia": resultado.dicas_ia or [],
                    "resumo_geral": resultado.resumo_geral,
                }},
            )

        except Exception as e:
            await db["documentos"].update_one(
                {"_id": ObjectId(documento_id)},
                {"$set": {"status": "erro", "erro": str(e)}},
            )
            print(f"[ERRO BG {documento_id[:8]}] {e}")

    async def buscar(self, documento_id: str) -> dict:
        db = get_async_db()
        try:
            doc = await db["documentos"].find_one({"_id": ObjectId(documento_id)})
        except Exception:
            raise HTTPException(400, detail="ID inválido.")
        if not doc:
            raise HTTPException(404, detail="Documento não encontrado.")
        doc["documento_id"] = str(doc.pop("_id"))
        return doc


def _veredicto(r) -> str:
    problemas = sum([
        bool(r.trechos_ia),
        bool(r.trechos_plagio),
        bool(r.trechos_fake_news),
    ])
    if problemas == 0:
        return "limpo"
    if problemas > 1:
        return "multiplos_problemas"
    if r.trechos_ia:
        return "suspeito_ia"
    if r.trechos_plagio:
        return "plagio"
    return "fake_news"
