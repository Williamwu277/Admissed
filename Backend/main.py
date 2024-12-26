from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from server import Server
from typing import List
import uvicorn
import json


app = FastAPI()
server = Server()

# TODO: Figure out proper headers to allow

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)


@app.post("/api/upload_spreadsheet")
def get_spreadsheet(data: UploadFile = File(...), ids: List[str] = Form(...)):
    
    # TODO: Santitization 
    # * limit file size
    # * check file type
    
    return server.upload_data(data.file, ids)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)