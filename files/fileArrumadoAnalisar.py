from fileManagement import FileManagement
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

class FileArrumadoAnalisar:
    def __init__(self, file_management: FileManagement):
        self.file_management = file_management

    def process_file(self, file_id: str):
        text = self.file_management.get_file(file_id)
        if text is None:
            return {"error": "File not found"}
        else:
            return text["data"]
        
    def chuncking(self):
        text = self.process_file()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=3500, chunk_overlap=600, separators=["\n\n", "\n", " ", ""])
        chunks = text_splitter.split_text(self.process_file(text))
        return chunks
    
    def embeddings(self):
        self.chunks = self.chuncking()
        model_name = "sentence-transformers/all-mpnet-base-v2"
        model_kwargs = {"device": "cpu"}
        encode_kwargs = {"normalize_embeddings": False}

        hf = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
        )

        texts = self.chunks
        embedding = hf.embed_documents(texts)

        return embedding
    
    def enumerate_chunks(self):
        self.chunks = self.chuncking()
        enumerated_chunks = list(enumerate(self.chunks))
        return enumerated_chunks
    
    
    

        



