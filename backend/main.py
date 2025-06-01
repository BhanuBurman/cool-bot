import uvicorn
import shutil
import time
import os
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
from starlette.middleware.cors import CORSMiddleware

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

DOCUMENT_PATH="documents/latest.pdf"

retriever = None
doc_chain = None




@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    async def event_generator():
        global retriever, doc_chain

        yield {"event": "status", "data": "Uploading file..."}
        time.sleep(0.5)

        with open(DOCUMENT_PATH, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        yield {"event": "status", "data": "File saved. Starting embedding..."}

        retriever = create_retriever(DOCUMENT_PATH)
        yield {"event": "status", "data": "Retriever created. Creating QA chain..."}

        doc_chain = create_doc_qa_chain(retriever)
        yield {"event": "status", "data": "QA chain ready. You can start chatting!"}

    return EventSourceResponse(event_generator())


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
