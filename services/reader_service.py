"""
Extrai texto de arquivos enviados pelo usuário.
Suporta: .txt, .pdf, .docx
"""
import io
from fastapi import UploadFile


class ReaderService:

    @staticmethod
    async def extrair_texto(file: UploadFile) -> str:
        conteudo = await file.read()
        nome = (file.filename or "").lower()

        if nome.endswith(".pdf"):
            return ReaderService._pdf(conteudo)
        elif nome.endswith(".docx"):
            return ReaderService._docx(conteudo)
        else:
            # Tenta UTF-8, cai para latin-1
            try:
                return conteudo.decode("utf-8")
            except UnicodeDecodeError:
                return conteudo.decode("latin-1", errors="replace")

    @staticmethod
    def _pdf(data: bytes) -> str:
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(data))
            paginas = [p.extract_text() or "" for p in reader.pages]
            return "\n\n".join(paginas)
        except Exception as e:
            raise ValueError(f"Erro ao ler PDF: {e}")

    @staticmethod
    def _docx(data: bytes) -> str:
        try:
            import docx
            doc = docx.Document(io.BytesIO(data))
            return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
        except Exception as e:
            raise ValueError(f"Erro ao ler DOCX: {e}")
