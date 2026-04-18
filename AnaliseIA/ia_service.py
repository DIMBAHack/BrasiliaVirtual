import os
import json
from AnaliseIA.core.config import settings
from services.agents_service import AgentsService as Agents
from langchain_core.messages import SystemMessage, HumanMessage


def _carregar_prompt(nome_arquivo: str) -> str:
    caminho = os.path.join(os.path.dirname(__file__), '..', 'prompts', nome_arquivo)
    with open(caminho, 'r', encoding='utf-8') as f:
        return f.read()


class IAService:
    def __init__(self):
        self.client = Agents().gpt_agent()
        self.prompt_detector = _carregar_prompt('detector_ia.txt')
        self.prompt_avaliador = _carregar_prompt('avaliador_fontes.txt')

    async def analisar_texto(self, texto_chunk: str) -> dict:
        try:
            messages = [
                SystemMessage(content=self.prompt_detector),
                HumanMessage(content=f"Analise o seguinte trecho:\n\n{texto_chunk}")
            ]

            response = await self.client.ainvoke(messages)
            return json.loads(response.content)

        except Exception as e:
            print(f"Erro interno na análise de IA: {e}")
            raise e

    async def avaliar_dominio(self, dominio: str, trecho_copiado: str) -> dict:
        try:
            messages = [
                SystemMessage(content=self.prompt_avaliador),
                HumanMessage(content=f"Domínio: {dominio}\nTrecho: {trecho_copiado}")
            ]

            response = await self.client.ainvoke(messages)
            return json.loads(response.content)

        except Exception as e:
            print(f"Erro interno na avaliação de domínio: {e}")
            raise e