#Sistema
import os
import re
import math
import time
import difflib
import logging
import warnings

#----------------------------------------------------------------
from typing import Optional
from dataclasses import dataclass, field
from dotenv import load_dotenv

#Internos criados
from services.reader_service import ReaderService
from services.agents_service import AgentsService
from chunk_service import ChunkService

#----------------------------------------------------------------
from langchain_core.messages import HumanMessage, SystemMessage
import torch
import numpy as np
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

# Parte de NLP
import nltk
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.WARNING)

# Natural Language Toolkit (NLTK) para tokenização recursos necessários para análise
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt", quiet=True)
try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab", quiet=True)

@dataclass
class TrechoAnalise:
    texto: str
    classificacao: str          # "ia", "plagio", "fake_news", "autoral"
    confianca: float            # 0.0 a 1.0
    evidencias: list = field(default_factory=list)  # links de plágio ou fontes de IA
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

class GeradorPrompts:
    def __init__(self):
        self.llm = AgentsService.claude_agent

    def gerar(self, tema: str, num_prompts: int = 4) -> list[str]:

        system = (
            """Você é um especialista em comportamento de estudantes universitários.
            Gere prompts REALISTAS que um aluno brasileiro usaria em IAs para
            fazer seu trabalho acadêmico. Os prompts devem ser variados: 
            um simples, um com pedido de introdução, um com estrutura completa,
            e um técnico/detalhado. Retorne SOMENTE os prompts, um por linha, "
            "numerados de 1 a """ + str(num_prompts) + "."
        )
        humano = f"Tema do trabalho: {tema}"

        resposta = self.llm.invoke([
            SystemMessage(content=system),
            HumanMessage(content=humano)
        ])

        linhas = resposta.content.strip().split("\n")
        prompts = []
        for linha in linhas:
            linha = re.sub(r"^\d+[\.\)]\s*", "", linha).strip()
            if linha and len(linha) > 10:
                prompts.append(linha)

        return prompts[:num_prompts]

class SimuladorRespostasIA:
    def __init__(self):
        self.anthropic = AgentsService.claude_agent
        self.openai = AgentsService.gpt_agent
        self.google = AgentsService.google_agent

    def simular_claude(self, prompt: str) -> Optional[str]:
        try:
            client = self.anthropic(
                max_tokens=800,
                messages=[{"role": "user", "content": prompt}]
            )
            return client.content[0].text
        except Exception as e:
            logging.warning(f"Claude simulação falhou: {e}")
            return None

    def simular_gpt(self, prompt: str) -> Optional[str]:
        try:
            client = self.openai()
            resp = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
            )
            return resp.choices[0].message.content
        except Exception as e:
            logging.warning(f"GPT simulação falhou: {e}")
            return None

    def simular_gemini(self, prompt: str) -> Optional[str]:
        try:
            model = AgentsService.google_agent()
            resp = model.generate_content(prompt)
            return resp.text
        except Exception as e:
            logging.warning(f"Gemini simulação falhou: {e}")
            return None

    def coletar_todas(self, prompts: list[str]) -> list[str]:
        respostas = []
        for prompt in prompts:
            for fn in [self.simular_claude, self.simular_gpt, self.simular_gemini]:
                r = fn(prompt)
                if r:
                    respostas.append(r)
                time.sleep(0.3)  
        return respostas

class AnalisadorPerplexidade:

    def __init__(self):
        self.modelo_carregado = False
        self.model = None
        self.tokenizer = None

    def carregar_modelo(self, callback=None):
        if self.modelo_carregado:
            return
        try:
            from transformers import GPT2LMHeadModel, GPT2TokenizerFast
            if callback:
                callback("Carregando modelo GPT-2 para análise de perplexidade...")
            self.tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
            self.model = GPT2LMHeadModel.from_pretrained("gpt2")
            self.model.eval()
            self.modelo_carregado = True
        except Exception as e:
            logging.warning(f"Não foi possível carregar GPT-2: {e}")

    def calcular_perplexidade(self, texto: str) -> float:
        if not self.modelo_carregado or not self.model:
            return -1.0

        try:
            tokens = self.tokenizer.encode(texto[:2000], return_tensors="pt")
            if tokens.shape[1] < 10:
                return -1.0

            with torch.no_grad():
                outputs = self.model(tokens, labels=tokens)
                loss = outputs.loss
                perplexidade = math.exp(loss.item())
            return perplexidade
        except Exception:
            return -1.0

    def classificar(self, perplexidade: float) -> tuple[str, float]:
        if perplexidade < 0:
            return "indeterminado", 0.0
        if perplexidade < 40:
            return "provavel ia", 0.85
        elif perplexidade < 70:
            return "baixa probabilidade de ia", 0.60
        elif perplexidade < 120:
            return "inconclusivo", 0.40
        else:
            return "provavel humano", 0.75

class ComparadorSimilaridade:

    @staticmethod
    def similaridade_tfidf(trecho: str, referencias: list[str]) -> float:

        if not referencias:
            return 0.0
        try:
            corpus = [trecho] + referencias
            vec = TfidfVectorizer(
                ngram_range=(1, 3),   
                min_df=1,
                stop_words=None     
            ).fit_transform(corpus)

            sims = cosine_similarity(vec[0:1], vec[1:])
            return float(sims.max())
        except Exception:
            return 0.0

    @staticmethod
    def similaridade_sequencia(trecho: str, referencias: list[str]) -> float:
        max_sim = 0.0
        for ref in referencias:
            ratio = difflib.SequenceMatcher(None, trecho.lower(), ref.lower()).ratio()
            max_sim = max(max_sim, ratio)
        return max_sim

    @staticmethod
    def combinar(sim_tfidf: float, sim_seq: float) -> float:
        """Combina as duas métricas com pesos."""
        return (sim_tfidf * 0.6) + (sim_seq * 0.4)

class DetectorPlagio:
#MUDAR PRA COPYLEAKS DEPOIS AQUI MATHEUS PLEASE 
    def __init__(self):
        self.ddgs = DDGS()

    def verificar_trecho(self, trecho: str) -> list[dict]:
        palavras = trecho.split()[:15]
        query = " ".join(palavras)

        fontes_encontradas = []
        try:
            resultados = list(self.ddgs.text(
                f'"{query}"',   
                max_results=3,
                region="br-pt"
            ))
            for r in resultados:
                sim = difflib.SequenceMatcher(
                    None,
                    trecho.lower()[:300],
                    r.get("body", "").lower()[:300]
                ).ratio()

                if sim > 0.35:  
                    fontes_encontradas.append({
                        "url": r.get("href", ""),
                        "titulo": r.get("title", ""),
                        "trecho_fonte": r.get("body", "")[:200],
                        "similaridade": round(sim * 100, 1)
                    })
        except Exception as e:
            logging.warning(f"Busca web falhou: {e}")

        return fontes_encontradas


class VerificadorFakeNews:
        
    def __init__(self):
        self.client = AgentsService.claude_agent()
 
    def verificar(self, trecho: str, tema: str) -> tuple[bool, str]:
        prompt = f"""Você é um verificador de fatos acadêmico rigoroso.
Tema do trabalho: {tema}
 
Analise o trecho abaixo e determine:
1. Há afirmações factualmente incorretas, inventadas ou sem base?
2. Se sim, explique brevemente qual informação está errada e por quê.
 
Responda APENAS neste formato JSON:
{{"fake": true/false, "explicacao": "texto curto ou vazio"}}
 
Trecho: {trecho[:500]}"""

        try:
            msg = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}]
            )
            import json
            texto = msg.content[0].text.strip()
            match = re.search(r"\{.*\}", texto, re.DOTALL)
            if match:
                dados = json.loads(match.group())
                return dados.get("fake", False), dados.get("explicacao", "")
        except Exception as e:
            logging.warning(f"Verificação de fatos falhou: {e}")

        return False, ""

from datetime import datetime
from dataclasses import asdict
from core.configDB import ConfigDB

class DMBAnalyzer:
    THRESHOLD_IA = 0.75 #msm q 75% pra min de IA prob

    def __init__(self, callback_status=None):
        self.cb = callback_status or (lambda msg: print(f"[DMB] {msg}"))
        self.leitor       = ReaderService.get_file_content()
        self.segmentador  = ChunkService.buscar_chunks()
        self.gerador      = GeradorPrompts()
        self.simulador    = SimuladorRespostasIA()
        self.perplexidade = AnalisadorPerplexidade()
        self.comparador   = ComparadorSimilaridade()
        self.plagio       = DetectorPlagio()
        self.fakenews     = VerificadorFakeNews()
        self.db           = ConfigDB().analiseDB()

    def salvar_analise(
        self,
        resultado: ResultadoAnalise,
        arquivo: str,
        tema: str,
        documento_id: str = None
    ) -> str:
        colecao = self.db["analises"]

        documento = {
            "documento_id": documento_id,
            "arquivo": arquivo,
            "tema": tema,
            "criado_em": datetime.now41(),
            "resumo": {
                "perplexidade_media": round(resultado.perplexidade_media, 2),
                "similares_ia_pct": round(resultado.similares_ia_pct, 2),
                "resumo_geral": resultado.resumo_geral,
            },
            "contagens": {
                "trechos_ia": len(resultado.trechos_ia),
                "trechos_plagio": len(resultado.trechos_plagio),
                "trechos_fake_news": len(resultado.trechos_fake_news),
                "trechos_autorais": len(resultado.trechos_autorais),
            },
            "trechos": {
                "ia": [asdict(t) for t in resultado.trechos_ia],
                "plagio": [asdict(t) for t in resultado.trechos_plagio],
                "fake_news": [asdict(t) for t in resultado.trechos_fake_news],
                "autorais": [asdict(t) for t in resultado.trechos_autorais],
            }
        }

        result = colecao.insert_one(documento)
        analise_id = str(result.inserted_id)
        self.cb(f"Análise salva no MongoDB com id: {analise_id}")
        return analise_id

    def analisar(self, caminho_arquivo: str, tema: str, documento_id: str = None) -> ResultadoAnalise:
        resultado = ResultadoAnalise()

        self.cb("Lendo o documento...")
        texto_completo = self.leitor.ler(caminho_arquivo)
        if not texto_completo.strip():
            raise ValueError("Documento vazio ou não legível.")

        self.cb("Realizando o chuncking do texto...")
        trechos = self.segmentador.segmentar(texto_completo)
        self.cb(f"   → {len(trechos)} trechos identificados.")

        self.cb("DMB AI gerando prompts baseados no tema...")
        try:
            prompts = self.gerador.gerar(tema, num_prompts=4)
            self.cb(f"   → {len(prompts)} prompts gerados.")
        except Exception as e:
            self.cb(f"Geração de prompts falhou: {e}")
            prompts = [f"Escreva um trabalho completo sobre: {tema}"]

        self.cb("Consultando GPT, Claude e Gemini com os prompts...")
        respostas_ia = self.simulador.coletar_todas(prompts)
        self.cb(f"   → {len(respostas_ia)} respostas coletadas das IAs.")

        self.perplexidade.carregar_modelo(callback=self.cb)

        total = len(trechos)
        perplexidades = []

        for i, trecho in enumerate(trechos):
            self.cb(f"Analisando trecho {i+1}/{total}...")

            perplex = self.perplexidade.calcular_perplexidade(trecho)
            if perplex > 0:
                perplexidades.append(perplex)
            classe_perplex, conf_perplex = self.perplexidade.classificar(perplex)

            sim_tfidf = self.comparador.similaridade_tfidf(trecho, respostas_ia)
            sim_seq   = self.comparador.similaridade_sequencia(trecho, respostas_ia)
            sim_final = self.comparador.combinar(sim_tfidf, sim_seq)

            # Classificação IA
            if sim_final >= self.THRESHOLD_IA or classe_perplex == "ia":
                confianca = max(sim_final, conf_perplex)
                resultado.trechos_ia.append(TrechoAnalise(
                    texto=trecho,
                    classificacao="ia",
                    confianca=round(confianca, 2),
                    detalhes=f"Similaridade: {round(sim_final*100,1)}% | Perplexidade: {round(perplex,1)}"
                ))
                continue

            # Plágio
            fontes = self.plagio.verificar_trecho(trecho)
            if fontes:
                resultado.trechos_plagio.append(TrechoAnalise(
                    texto=trecho,
                    classificacao="plagio",
                    confianca=round(fontes[0]["similaridade"] / 100, 2),
                    evidencias=[f["url"] for f in fontes],
                    detalhes=f"{len(fontes)} fonte(s) encontrada(s)"
                ))
                continue

            # Fake news
            is_fake, explicacao = self.fakenews.verificar(trecho, tema)
            if is_fake:
                resultado.trechos_fake_news.append(TrechoAnalise(
                    texto=trecho,
                    classificacao="fake_news",
                    confianca=0.80,
                    detalhes=explicacao
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
        total_trechos = total or 1
        resultado.similares_ia_pct = round(len(resultado.trechos_ia) / total_trechos * 100, 1)

        # Salva no MongoDB
        self.cb("Salvando análise no banco de dados...")
        analise_id = self.salvar_analise(resultado, caminho_arquivo, tema, documento_id)
        resultado.resumo_geral = f"Análise concluída. ID: {analise_id}"

        return resultado