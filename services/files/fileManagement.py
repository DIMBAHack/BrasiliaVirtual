from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from database.configDB import ConfigDB
from bson import ObjectId

app = FastAPI()
db_config = ConfigDB()


class FileManagement:
    def __init__(self):
        self.file_collection = db_config.fileDB()["files"]

    async def upload_file(self, file: UploadFile) -> str:
        text_coded = await file.read()
        text_decoded = text_coded.decode("utf-8", errors="replace")

        result = self.file_collection.insert_one({
            "filename": file.filename,
            "contentType": file.content_type,
            "data": text_decoded
        })

        return str(result.inserted_id)

    def get_file(self, file_id: str) -> dict | None:
        return self.file_collection.find_one({"_id": ObjectId(file_id)})

    def get_file_content(self, file_id: str) -> str | None:
        doc = self.get_file(file_id)
        return doc["data"] if doc else None

    def files_list(self) -> list[dict]:
        return list(self.file_collection.find())