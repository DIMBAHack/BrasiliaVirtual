"""
Divide texto em chunks para análise.
Remove dependência de Redis — usa memória.
"""
from langchain_text_splitters import RecursiveCharacterTextSplitter


class ChunkService:
    _splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    @classmethod
    def dividir(cls, texto: str) -> list[str]:
        if not texto or not texto.strip():
            return []
        chunks = cls._splitter.split_text(texto)
        # Filtra chunks muito curtos (< 80 chars) — pouco conteúdo para análise
        return [c for c in chunks if len(c.strip()) >= 80]
