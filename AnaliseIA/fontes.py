from services.files.fileManagement import fileArrumadoAnalisar
from database.configDB import ConfigDB
import os
from services.agents_service import Agents

class Fontes:
    def __init__(self):
        self.file = fileArrumadoAnalisar.chuncking()

    def find_references(self):
        referencias = {}
        agent = Agents.google_agent(self=Agents)
        formatted_chunks = self.format_chunks()

        for chunk in formatted_chunks:
            chunk_number = chunk["chunk_number"]
            chunk_text = chunk["text"]

            mensagens = [
                ("system", """Você é um agente que tem como objetivo encontrar as referências utilizadas em um texto.
                O texto pode apresentar referências como 'assim como visto em [referencia]', 'conforme mencionado em [referencia]',
                'de acordo com [referencia]', ou até mesmo no padrão ABNT.   
                Sua tarefa é identificar e extrair essas referências do texto fornecido.
                Retorne apenas as referências encontradas, cada uma no formato:
                'nome: [nome do autor], titulo: [titulo do artigo], ano: [ano de publicação], link: [link da referencia]'
                
                Se não houver referências, retorne exatamente: 'NENHUMA_REFERENCIA'"""),
                ("human", chunk_text)
            ]

            resposta = agent.invoke({"messages": mensagens})
            resultado = resposta["messages"][-1].content

            if "NENHUMA_REFERENCIA" not in resultado:
                referencias[chunk_number] = {
                    "chunk_text": chunk_text,
                    "referencias": resultado
                }

        return referencias       