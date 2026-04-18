from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from services.files.fileManagement import FileManagement

router = APIRouter(prefix="/files", tags=["Files"])
file_management = FileManagement()

class Routes:
    def __init__(self):
        self.router = router
        self.file_management = file_management

    @router.post("/upload/")
    async def upload_file(self, file: UploadFile = File(...)):
        file_id = await self.file_management.upload_file(file)
        return {"file_id": file_id, "filename": file.filename}
        

    @router.get("/download/{file_id}")
    async def download_file(file_id: str):
        file_doc = file_management.get_file(file_id)
        if not file_doc:
            raise HTTPException(status_code=404, detail="Arquivo não encontrado")

        return StreamingResponse(
            iter([file_doc["data"]]),
            media_type=file_doc["contentType"],
            headers={"Content-Disposition": f"attachment; filename={file_doc['filename']}"}
        )


    @router.get("/content/{file_id}")
    async def get_file_content(file_id: str):
        content = file_management.get_file_content(file_id)
        if not content:
            raise HTTPException(status_code=404, detail="Arquivo não encontrado")

        return {"file_id": file_id, "content": content}


    @router.get("/list/")
    async def list_files():
        files = file_management.files_list()
        return {
            "total": len(files),
            "files": [
                {"file_id": str(f["_id"]), "filename": f["filename"], "contentType": f["contentType"]}
                for f in files
            ]
        }


    @router.delete("/delete/{file_id}")
    async def delete_file(file_id: str):
        file_doc = file_management.get_file(file_id)
        if not file_doc:
            raise HTTPException(status_code=404, detail="Arquivo não encontrado")

        file_management.file_collection.delete_one({"_id": file_doc["_id"]})
        return {"message": f"Arquivo {file_doc['filename']} deletado com sucesso"}