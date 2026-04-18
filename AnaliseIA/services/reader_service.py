import io
import pdfplumber
from docx import Document
from fastapi import UploadFile, HTTPException


class ReaderService:
    async def extract(self, file: UploadFile) -> str:
        file_bytes = await file.read()
        extension = file.filename.split(".")[-1].lower()

        if extension == "pdf":
            return self._read_pdf(file_bytes)
        elif extension in ("docx", "doc"):
            return self._read_docx(file_bytes)
        elif extension in ("txt", "md"):
            return self._read_txt(file_bytes)
        else:
            raise HTTPException(
                status_code=415,
                detail=f"Tipo de arquivo não suportado: .{extension}"
            )

    def _read_pdf(self, file_bytes: bytes) -> str:
        text_parts = []
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        return "\n".join(text_parts)

    def _read_docx(self, file_bytes: bytes) -> str:
        doc = Document(io.BytesIO(file_bytes))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n".join(paragraphs)

    def _read_txt(self, file_bytes: bytes) -> str:
        return file_bytes.decode("utf-8", errors="replace")