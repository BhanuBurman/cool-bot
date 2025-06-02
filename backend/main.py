from typing import List

import uvicorn
import shutil
import time
import os
from fastapi import Request, Depends
from fastapi.responses import JSONResponse
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from starlette.middleware.cors import CORSMiddleware

import crud
import models
import schemas
from database import engine, Base, SessionLocal
from models import FileInfo
from new_llm import create_retriever, create_doc_qa_chain, chat_func, create_general_chain


app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

class FileNameRequest(BaseModel):
    file_name: str

UPLOAD_DIR="documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)

retriever = None
doc_chain = None
DOCUMENT_PATH=None


# Create tables
models.Base.metadata.create_all(bind=engine)
# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/get-all-files", response_model=List[schemas.FileInfoResponse])
def get_all_files(db: Session = Depends(get_db)):
    return crud.fetch_all_files(db)

@app.post("/upload_info/", response_model=schemas.FileInfoResponse)
def upload_info(file:schemas.FileInfoCreate, db:Session  = Depends(get_db)):
    return crud.create_file_info(db, file)

@app.post("/upload/")
def upload_file(file: UploadFile = File(...)):
    global retriever, doc_chain, DOCUMENT_PATH
    DOCUMENT_PATH = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(DOCUMENT_PATH, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    except Exception as e:
        return {"error": str(e)}
    return {"status":f"Uploaded successfully", "fileName":file.filename}

@app.post("/embed_file")
def embed_file(req: FileNameRequest):
    global retriever, doc_chain, DOCUMENT_PATH
    if str is None:
        return {"error": "No document path provided"}

    DOCUMENT_PATH = os.path.join(UPLOAD_DIR, req.file_name)

    print("Document Uploaded...")
    retriever = create_retriever(DOCUMENT_PATH)
    print("Created Retriever...")
    doc_chain = create_doc_qa_chain(retriever)
    print("Document Chain Created...")
    return {"status":"Document embedded successfully"}

chat_history = []
@app.post("/generate")
def get_response(req:QueryRequest):
    # print(req)
    general_chain = create_general_chain()
    result = chat_func(req.query, doc_chain, general_chain, chat_history)
    return {"response": result}

@app.get("/refresh")
def clear_chat_history():
    chat_history.clear()




if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
