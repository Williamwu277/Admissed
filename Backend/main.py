from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from server import Server
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
def get_spreadsheet(data: UploadFile = File(...)):
    
    # TODO: Santitization 
    # * limit file size
    # * check file type

    server.upload_data(data.file)


@app.get("/api/get_data")
def get_data():

    # TODO: return only say 1000 results at a time

    data = server.get_data()
    return data


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)