"""
Motor principal de análise DIMBA.
Detecta: geração por IA, plágio, fake news, ou conteúdo autoral.
Se houver IA detectada, gera dicas pedagógicas de uso ético.
"""
import os
import re
import math
import time
import difflib
import logging
import warnings
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage

import nltk
import numpy as np
import torch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from duckduckgo_search import DDGS

from services.agents_service import AgentsService

load_dotenv()
warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Baixa recursos NLTK se necessário
for recurso in ["punkt", "punkt_tab"]:
    try:
        nltk.data.find(f"tokenizers/{recurso}")
    except LookupError:
        nltk.download(recurso, quiet=True)


# ──────────────────────────────────────────────────
# Dataclasses de resultado
# ──────────────────────────────────────────────────

@dataclass
class TrechoAnalise:
    texto: str
    classificacao: str       # "ia" | "plagio" | "fake_news" | "autoral"
    confianca: float         # 0.0–1.0
    evidencias: list = field(default_factory=list)
    detalhes: str = ""


@dataclass
class ResultadoAnalise:
    trechos_ia: list = field(default_factory=list)
    trechos_plagio: list = field(default_factory=list)
    trechos_fake_news: list = field(default_factory=list)
    trechos_autorais: list = field(default_factory=list)
    resumo_geral: str = ""
    perplexidade_media: float = 0.0
    similares_ia_pct: float = 0.0
    dicas_ia: list = field(default_factory=list)


# ──────────────────────────────────────────────────
# Gerador de prompts realistas de alunos
# ──────────────────────────────────────────────────

class GeradorPrompts:
    def __init__(self):
        self._llm = None

    @property
    def llm(self):
        if self._llm is None:
            self._llm = AgentsService.claude_agent()
        return self._llm

    def gerar(self, tema: str, num_prompts: int = 3) -> list[str]:
        system = (
            "Você é um especialista em comportamento de estudantes universitários brasileiros. "
            "Gere prompts REALISTAS que um aluno usaria em uma IA para fazer seu trabalho. "
            f"Retorne SOMENTE {num_prompts} prompts, um por linha, numerados."
        )
        try:
            resposta = self.llm.invoke([
                SystemMessage(content=system),
                HumanMessage(content=f"Tema: {tema}"),
            ])
            linhas = resposta.content.strip().split("\n")
            prompts = [re.sub(r"^\d+[\.\)]\s*", "", l).strip() for l in linhas if len(l.strip()) > 10]
            return prompts[:num_prompts]
        except Exception as e:
            logger.warning(f"GeradorPrompts falhou: {e}")
            return [f"Escreva um trabalho completo sobre: {tema}"]


# ──────────────────────────────────────────────────
# Simulador de respostas de IAs
# ──────────────────────────────────────────────────

class SimuladorRespostasIA:

    def _invocar(self, agente_fn, prompt: str) -> Optional[str]:
        try:
            modelo = agente_fn()
            resposta = modelo.invoke([HumanMessage(content=prompt)])
            return resposta.content
        except Exception as e:
            logger.warning(f"Simulação falhou ({agente_fn.__name__}): {e}")
            return None

    def coletar_todas(self, prompts: list[str]) -> list[str]:
        respostas = []
        agentes = [AgentsService.claude_agent, AgentsService.gpt_agent, AgentsService.google_agent]
        for prompt in prompts:
            for agente_fn in agentes:
                r = self._invocar(agente_fn, prompt)
                if r:
                    respostas.append(r)
                time.sleep(0.2)
        return respostas


# ──────────────────────────────────────────────────
# Analisador de perplexidade (GPT-2 local)
# ──────────────────────────────────────────────────

class AnalisadorPerplexidade:
    def __init__(self):
        self.model = None
        self.tokenizer = None

    def carregar(self, cb=None):
        if self.model:
            return
        try:
            from transformers import GPT2LMHeadModel, GPT2TokenizerFast
            if cb:
                cb("Carregando modelo GPT-2...")
            self.tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
            self.model = GPT2LMHeadModel.from_pretrained("gpt2")
            self.model.eval()
        except Exception as e:
            logger.warning(f"GPT-2 não carregado: {e}")

    def calcular(self, texto: str) -> float:
        if not self.model:
            return -1.0
        try:
            tokens = self.tokenizer.encode(texto[:2000], return_tensors="pt")
            if tokens.shape[1] < 10:
                return -1.0
            with torch.no_grad():
                loss = self.model(tokens, labels=tokens).loss
            return math.exp(loss.item())
        except Exception:
            return -1.0

    def classificar(self, p: float) -> tuple[str, float]:
        if p < 0:       return "indeterminado", 0.0
        if p < 40:      return "ia", 0.85
        if p < 70:      return "baixa_prob_ia", 0.55
        if p < 120:     return "inconclusivo", 0.40
        return "humano", 0.75


# ──────────────────────────────────────────────────
# Comparador de similaridade TF-IDF + sequencial
# ──────────────────────────────────────────────────

class ComparadorSimilaridade:

    @staticmethod
    def tfidf(trecho: str, refs: list[str]) -> float:
        if not refs:
            return 0.0
        try:
            corpus = [trecho] + refs
            vec = TfidfVectorizer(ngram_range=(1, 3)).fit_transform(corpus)
            return float(cosine_similarity(vec[0:1], vec[1:]).max())
        except Exception:
            return 0.0

    @staticmethod
    def sequencia(trecho: str, refs: list[str]) -> float:
        return max(
            (difflib.SequenceMatcher(None, trecho.lower(), r.lower()).ratio() for r in refs),
            default=0.0,
        )

    @classmethod
    def combinar(cls, trecho: str, refs: list[str]) -> float:
        s_tfidf = cls.tfidf(trecho, refs)
        s_seq = cls.sequencia(trecho, refs)
        return (s_tfidf * 0.6) + (s_seq * 0.4)


# ──────────────────────────────────────────────────
# Detector de plágio via DuckDuckGo
# ──────────────────────────────────────────────────

class DetectorPlagio:
    def __init__(self):
        self.ddgs = DDGS()

    def verificar(self, trecho: str) -> list[dict]:
        query = " ".join(trecho.split()[:12])
        fontes = []
        try:
            resultados = list(self.ddgs.text(f'"{query}"', max_results=3, region="br-pt"))
            for r in resultados:
                sim = difflib.SequenceMatcher(
                    None, trecho.lower()[:300], r.get("body", "").lower()[:300]
                ).ratio()
                if sim > 0.35:
                    fontes.append({
                        "url": r.get("href", ""),
                        "titulo": r.get("title", ""),
                        "similaridade": round(sim * 100, 1),
                    })
        except Exception as e:
            logger.warning(f"DuckDuckGo falhou: {e}")
        return fontes


# ──────────────────────────────────────────────────
# Verificador de fake news via Claude
# ──────────────────────────────────────────────────

class VerificadorFakeNews:
    def __init__(self):
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = AgentsService.claude_agent()
        return self._client

    def verificar(self, trecho: str, tema: str) -> tuple[bool, str]:
        prompt = f"""Você é um verificador de fatos acadêmico.
Tema: {tema}

Analise se o trecho abaixo contém afirmações factualmente incorretas ou inventadas.
Responda SOMENTE em JSON: {{"fake": true/false, "explicacao": "texto curto ou vazio"}}

Trecho: {trecho[:500]}"""
        try:
            import json
            resposta = self.client.invoke([HumanMessage(content=prompt)])
            match = re.search(r"\{.*\}", resposta.content, re.DOTALL)
            if match:
                dados = json.loads(match.group())
                return dados.get("fake", False), dados.get("explicacao", "")
        except Exception as e:
            logger.warning(f"FakeNews check falhou: {e}")
        return False, ""


# ──────────────────────────────────────────────────
# Gerador de dicas pedagógicas
# ──────────────────────────────────────────────────

class GeradorDicasIA:
    def __init__(self):
        self._llm = None

    @property
    def llm(self):
        if self._llm is None:
            self._llm = AgentsService.claude_agent()
        return self._llm

    def gerar(self, tema: str, pct_ia: float) -> list[str]:
        prompt = f"""Um trabalho acadêmico sobre '{tema}' teve {pct_ia:.0f}% do conteúdo
identificado como provavelmente gerado por IA.

Gere 5 dicas PRÁTICAS e EDUCATIVAS sobre como o estudante pode usar IA de forma
ética e produtiva — como ferramenta de apoio, sem copiar e colar respostas prontas.
Foque em técnicas como: prompts de pesquisa, revisão crítica, síntese, brainstorming.

Retorne as 5 dicas numeradas, cada uma em uma linha, sem títulos."""
        try:
            resposta = self.llm.invoke([HumanMessage(content=prompt)])
            linhas = resposta.content.strip().split("\n")
            dicas = [re.sub(r"^\d+[\.\)]\s*", "", l).strip() for l in linhas if l.strip()]
            return [d for d in dicas if len(d) > 20][:5]
        except Exception as e:
            logger.warning(f"GeradorDicasIA falhou: {e}")
            return [
                "Use a IA para gerar perguntas sobre o tema, não respostas prontas.",
                "Peça à IA que explique conceitos difíceis, depois reescreva com suas palavras.",
                "Use IA para criar um esquema de tópicos e desenvolva cada ponto você mesmo.",
                "Peça sugestões de fontes e referências, depois leia os originais.",
                "Use IA para revisar seu texto e melhorar a clareza, não para escrevê-lo.",
            ]


# ──────────────────────────────────────────────────
# Orquestrador principal: DMBAnalyzer
# ──────────────────────────────────────────────────

class DMBAnalyzer:
    THRESHOLD_IA = 0.72

    def __init__(self, callback_status=None):
        self.cb = callback_status or (lambda msg: print(f"[DMB] {msg}"))
        self.gerador_prompts  = GeradorPrompts()
        self.simulador        = SimuladorRespostasIA()
        self.perplexidade     = AnalisadorPerplexidade()
        self.comparador       = ComparadorSimilaridade()
        self.plagio           = DetectorPlagio()
        self.fakenews         = VerificadorFakeNews()
        self.dicas_ia         = GeradorDicasIA()

    def analisar(self, chunks: list[str], tema: str) -> ResultadoAnalise:
        resultado = ResultadoAnalise()

        if not chunks:
            raise ValueError("Nenhum trecho para analisar.")

        self.cb("Gerando prompts baseados no tema...")
        prompts = self.gerador_prompts.gerar(tema, num_prompts=3)
        self.cb(f"   → {len(prompts)} prompts gerados.")

        self.cb("Coletando respostas das IAs para referência...")
        respostas_ia = self.simulador.coletar_todas(prompts)
        self.cb(f"   → {len(respostas_ia)} respostas coletadas.")

        self.perplexidade.carregar(cb=self.cb)

        perplexidades = []
        total = len(chunks)

        for i, trecho in enumerate(chunks):
            self.cb(f"Analisando trecho {i + 1}/{total}...")

            # Perplexidade (GPT-2)
            perplex = self.perplexidade.calcular(trecho)
            if perplex > 0:
                perplexidades.append(perplex)
            classe_perplex, conf_perplex = self.perplexidade.classificar(perplex)

            # Similaridade com respostas de IA
            sim = self.comparador.combinar(trecho, respostas_ia) if respostas_ia else 0.0

            # ─ Classificação ─────────────────────────

            if sim >= self.THRESHOLD_IA or classe_perplex == "ia":
                confianca = max(sim, conf_perplex)
                resultado.trechos_ia.append(TrechoAnalise(
                    texto=trecho,
                    classificacao="ia",
                    confianca=round(confianca, 2),
                    detalhes=f"Similaridade: {round(sim * 100, 1)}% | Perplexidade: {round(perplex, 1)}",
                ))
                continue

            # Plágio
            fontes = self.plagio.verificar(trecho)
            if fontes:
                resultado.trechos_plagio.append(TrechoAnalise(
                    texto=trecho,
                    classificacao="plagio",
                    confianca=round(fontes[0]["similaridade"] / 100, 2),
                    evidencias=[f["url"] for f in fontes],
                    detalhes=f"{len(fontes)} fonte(s) similar(es) encontrada(s)",
                ))
                continue

            # Fake news
            is_fake, explicacao = self.fakenews.verificar(trecho, tema)
            if is_fake:
                resultado.trechos_fake_news.append(TrechoAnalise(
                    texto=trecho,
                    classificacao="fake_news",
                    confianca=0.80,
                    detalhes=explicacao,
                ))
                continue

            resultado.trechos_autorais.append(TrechoAnalise(
                texto=trecho,
                classificacao="autoral",
                confianca=0.90,
            ))

        # Métricas finais
        if perplexidades:
            resultado.perplexidade_media = sum(perplexidades) / len(perplexidades)

        total_nz = total or 1
        resultado.similares_ia_pct = round(len(resultado.trechos_ia) / total_nz * 100, 1)

        # Gera dicas se houver IA detectada
        if resultado.trechos_ia:
            self.cb("Gerando dicas pedagógicas sobre uso ético de IA...")
            resultado.dicas_ia = self.dicas_ia.gerar(tema, resultado.similares_ia_pct)

        resultado.resumo_geral = self._montar_resumo(resultado, total)
        return resultado

    @staticmethod
    def _montar_resumo(r: ResultadoAnalise, total: int) -> str:
        partes = []
        if r.trechos_ia:
            partes.append(f"{len(r.trechos_ia)} trecho(s) com provável geração por IA")
        if r.trechos_plagio:
            partes.append(f"{len(r.trechos_plagio)} trecho(s) com indícios de plágio")
        if r.trechos_fake_news:
            partes.append(f"{len(r.trechos_fake_news)} trecho(s) com possível fake news")
        if r.trechos_autorais:
            partes.append(f"{len(r.trechos_autorais)} trecho(s) considerados autorais")
        if not partes:
            return "Análise sem resultados."
        return f"De {total} trechos: " + "; ".join(partes) + "."
