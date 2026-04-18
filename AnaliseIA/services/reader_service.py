from fastapi import FastAPI, File, UploadFile
from core.configDB import ConfigDB
from fastapi.responses import StreamingResponse
import os

app = FastAPI()
client = ConfigDB.get_db_file(self=ConfigDB())
db = client["DMBAI"]


class ReaderService:
    def __init__(self, db):
        self.db = db

    @app.post("/upload/")
    async def upload_file(file: UploadFile = File(...)):
        text_coded = await file.read()
        text_decoded = text_coded.decode("utf-8", errors="replace")
        file_id = await db.fs.files.insert_one({
            "filename": file.filename,
            "contentType": file.content_type,
            "data": text_decoded
        })
        
        return {"file_id": str(file_id.inserted_id), "filename": file.filename}

    async def save_file(self, file: UploadFile):
        text_coded = await file.read()
        text_decoded = text_coded.decode("utf-8", errors="replace")
        file_id = await self.db.fs.files.insert_one({
            "filename": file.filename,
            "contentType": file.content_type,
            "data": text_decoded
        })
        return str(file_id.inserted_id)

    @app.get("/download/{file_id}")
    async def download_file(file_id: str):
        file_doc = await db.fs.files.find_one({"_id": file_id})
        if not file_doc:
            return {"error": "File not found"}
        
        return StreamingResponse(
            iter([file_doc["data"]]),
            media_type=file_doc["contentType"],
            headers={"Content-Disposition": f"attachment; filename={file_doc['filename']}"}
        )
    
    async def get_file(self, file_id: str):
        file_doc = await self.db.fs.files.find_one({"_id": file_id})
        if not file_doc:
            return None
        return file_doc
    
    async def get_file_content(self, file_id:str):
        self.file_doc = await self.db.fs.files.find_one({"_id": file_id})
        if not self.file_doc:
            return None
        return self.file_doc["data"]
    
    def files_list(self):
        files = self.db.fs.files.find()
        return files