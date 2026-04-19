import os
import re
import math
import time
import difflib
import logging
import warnings
import json
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

# Nota: AgentsService deve estar configurado no seu ambiente para chamar Claude/GPT
try:
    from services.agents_service import AgentsService
except ImportError:
    # Fallback caso o serviço não esteja definido
    class AgentsService:
        @staticmethod
        def claude_agent(): return None
        @staticmethod
        def gpt_agent(): return None
        @staticmethod
        def google_agent(): return None

load_dotenv()
warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Recursos NLTK
for recurso in ["punkt", "punkt_tab"]:
    try:
        nltk.data.find(f"tokenizers/{recurso}")
    except LookupError:
        nltk.download(recurso, quiet=True)

# ──────────────────────────────────────────────────
# DATACLASSES DE RESULTADO
# ──────────────────────────────────────────────────

@dataclass
class TrechoAnalise:
    texto: str
    classificacao: str       # "ia" | "plagio" | "fake_news" | "autoral"
    confianca: float         # 0.0–1.0
    perplexidade: float = 0.0
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
# COMPONENTES DE APOIO
# ──────────────────────────────────────────────────

class GeradorPrompts:
    def gerar(self, tema: str, num_prompts: int = 3) -> list[str]:
        llm = AgentsService.claude_agent()
        if not llm: return [f"Escreva sobre {tema}"]
        system = "Gere prompts REALISTAS de alunos universitários brasileiros. SOMENTE os prompts, um por linha."
        try:
            res = llm.invoke([SystemMessage(content=system), HumanMessage(content=f"Tema: {tema}")])
            return [re.sub(r"^\d+[\.\)]\s*", "", l).strip() for l in res.content.split("\n") if len(l) > 10][:num_prompts]
        except: return [f"Escreva um trabalho sobre {tema}"]

class SimuladorRespostasIA:
    def coletar_todas(self, prompts: list[str]) -> list[str]:
        respostas = []
        agentes = [AgentsService.claude_agent, AgentsService.gpt_agent, AgentsService.google_agent]
        for p in prompts:
            for a_fn in agentes:
                model = a_fn()
                if model:
                    try:
                        r = model.invoke([HumanMessage(content=p)])
                        respostas.append(r.content)
                    except: pass
        return respostas

class AnalisadorPerplexidade:
    def __init__(self):
        self.model = None
        self.tokenizer = None

    def carregar(self, cb=None):
        if self.model: return
        try:
            from transformers import GPT2LMHeadModel, GPT2TokenizerFast
            if cb: cb("Carregando GPT-2 local...")
            self.tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
            self.model = GPT2LMHeadModel.from_pretrained("gpt2")
            self.model.eval()
        except: pass

    def calcular(self, texto: str) -> float:
        if not self.model: return -1.0
        try:
            tokens = self.tokenizer.encode(texto[:1024], return_tensors="pt")
            with torch.no_grad():
                loss = self.model(tokens, labels=tokens).loss
            return math.exp(loss.item())
        except: return -1.0

    def classificar(self, p: float) -> tuple[str, float]:
        if p < 0: return "indeterminado", 0.0
        if p < 60: return "ia", 0.85
        return "humano", 0.70

class DetectorEstiloIA:
    VICIOS = [r"\bem suma\b", r"\bem conclusão\b", r"\bvale ressaltar\b", r"\balém disso\b", r"\bno que tange\b"]
    @classmethod
    def calcular(cls, texto: str) -> float:
        matches = sum(1 for p in cls.VICIOS if re.search(p, texto.lower()))
        return min(matches / 3, 1.0)

class DetectorPlagio:
    def verificar(self, trecho: str) -> list[dict]:
        try:
            with DDGS() as ddgs:
                res = list(ddgs.text(f'"{trecho[:80]}"', max_results=2, region="br-pt"))
                return [{"url": r["href"], "similaridade": 90} for r in res]
        except: return []

class VerificadorFakeNews:
    def verificar(self, trecho: str, tema: str) -> tuple[bool, str]:
        llm = AgentsService.claude_agent()
        if not llm: return False, ""
        prompt = f"Analise fatos: {trecho}. Responda JSON: {{\"fake\": bool, \"explicacao\": \"str\"}}"
        try:
            res = llm.invoke([HumanMessage(content=prompt)])
            dados = json.loads(re.search(r"\{.*\}", res.content, re.DOTALL).group())
            return dados.get("fake", False), dados.get("explicacao", "")
        except: return False, ""

class GeradorDicasIA:
    def gerar(self, tema: str, pct: float) -> list[str]:
        return [
            "Use a IA para estruturar tópicos, mas escreva o conteúdo final.",
            "Sempre verifique as referências citadas pela IA; elas podem ser inventadas.",
            "Trate a IA como um tutor de brainstorming, não como um autor substituto."
        ]

# ──────────────────────────────────────────────────
# MOTOR PRINCIPAL: DMBAnalyzer
# ──────────────────────────────────────────────────

class DMBAnalyzer:
    def __init__(self, callback_status=None):
        self.cb = callback_status or (lambda m: print(f"[DIMBA] {m}"))
        self.perplexidade = AnalisadorPerplexidade()
        self.gerador_prompts = GeradorPrompts()
        self.simulador = SimuladorRespostasIA()
        self.plagio = DetectorPlagio()
        self.fakenews = VerificadorFakeNews()
        self.gerador_dicas = GeradorDicasIA()

    def analisar(self, chunks: list[str], tema: str) -> ResultadoAnalise:
        resultado = ResultadoAnalise()
        chunks_validos = [c.strip() for c in chunks if len(c.split()) > 10]
        
        self.cb("Coletando referências de IA...")
        refs_ia = self.simulador.coletar_todas(self.gerador_prompts.gerar(tema, 1))
        self.perplexidade.carregar(self.cb)
        
        perplex_list = []
        for i, trecho in enumerate(chunks_validos):
            self.cb(f"Analisando trecho {i+1}/{len(chunks_validos)}")
            
            p_val = self.perplexidade.calcular(trecho)
            if p_val > 0: perplex_list.append(p_val)
            classe_p, conf_p = self.perplexidade.classificar(p_val)
            estilo = DetectorEstiloIA.calcular(trecho)
            
            # Decisão IA
            if classe_p == "ia" or estilo > 0.6:
                resultado.trechos_ia.append(TrechoAnalise(trecho, "ia", max(conf_p, estilo), p_val))
                continue
            
            # Plágio
            fontes = self.plagio.verificar(trecho)
            if fontes:
                resultado.trechos_plagio.append(TrechoAnalise(trecho, "plagio", 0.9, evidencias=[f["url"] for f in fontes]))
                continue
                
            resultado.trechos_autorais.append(TrechoAnalise(trecho, "autoral", 0.9, p_val))

        resultado.perplexidade_media = np.mean(perplex_list) if perplex_list else 0
        resultado.similares_ia_pct = (len(resultado.trechos_ia) / len(chunks_validos)) * 100
        resultado.resumo_geral = f"Concluído: {len(resultado.trechos_ia)} IA, {len(resultado.trechos_plagio)} Plágio."
        
        if resultado.similares_ia_pct > 20:
            resultado.dicas_ia = self.gerador_dicas.gerar(tema, resultado.similares_ia_pct)
            
        return resultado

# Exemplo de uso:
# analyzer = DMBAnalyzer()
# result = analyzer.analisar(["Texto longo aqui...", "Outro parágrafo..."], "Mudanças Climáticas")