import os
import json
from openai import AsyncOpenAI, RateLimitError, APIConnectionError
from core.config import settings


def _carregar_prompt(nome_arquivo: str) -> str:
    caminho = os.path.join(os.path.dirname(__file__), '..', 'prompts', nome_arquivo)
    with open(caminho, 'r', encoding='utf-8') as f:
        return f.read()


class IAService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.prompt_detector = _carregar_prompt('detector_ia.txt')
        self.prompt_avaliador = _carregar_prompt('avaliador_fontes.txt')

    async def analisar_texto(self, texto_chunk: str) -> dict:
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={"type": "json_object"},
                temperature=0.1,
                messages=[
                    {"role": "system", "content": self.prompt_detector},
                    {"role": "user", "content": f"Analise o seguinte trecho:\n\n{texto_chunk}"}
                ],
                timeout=15.0
            )
            return json.loads(response.choices[0].message.content)

        except RateLimitError as e:
            print("Alerta: Limite da OpenAI atingido (Rate Limit).")
            raise e
        except APIConnectionError as e:
            print("Erro de conexão com os servidores da OpenAI.")
            raise e
        except Exception as e:
            print(f"Erro interno na análise de IA: {e}")
            raise e

    async def avaliar_dominio(self, dominio: str, trecho_copiado: str) -> dict:
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={"type": "json_object"},
                temperature=0.1,
                messages=[
                    {"role": "system", "content": self.prompt_avaliador},
                    {"role": "user", "content": f"Domínio: {dominio}\nTrecho: {trecho_copiado}"}
                ],
                timeout=10.0
            )
            return json.loads(response.choices[0].message.content)

        except RateLimitError as e:
            print("Alerta: Limite da OpenAI atingido (Rate Limit).")
            raise e
        except APIConnectionError as e:
            print("Erro de conexão com os servidores da OpenAI.")
            raise e
        except Exception as e:
            print(f"Erro interno na avaliação de domínio: {e}")
            raise e