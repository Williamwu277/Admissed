from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from server import upload_data, generate_graphs
from typing import List, Dict
from pydantic import BaseModel
from mangum import Mangum
import uvicorn
import sys
import time


app = FastAPI()


# AWS Lambda handles CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)



class UserQuery(BaseModel):
    data: List[Dict[str, str]]
    main_query: Dict[str, str]
    filters: Dict[str, List[str]]


@app.post("/api/upload_spreadsheet")
def get_spreadsheet(data: UploadFile = File(...), ids: List[str] = Form(...)):
    
    # check file size and extension
    file_size_limit = 512 * 1024 # 500 KB
    file_len = len(data.file.read())
    if file_len > file_size_limit:
        raise HTTPException(status_code=413, detail="File Exceeds 500 KB")
    data.file.seek(0)

    if data.filename.rsplit(".", 1)[1].lower() != "csv" and "csv" in data.content_type:
        raise HTTPException(status_code=400, detail="CSV Files Only")
    
    ret = upload_data(data.file, ids)
    if ret["Status"] >= 400:
        raise HTTPException(status_code=ret["Status"], detail=ret["Description"])

    return ret["Description"]


@app.post("/api/get_graphs")
def get_graphs(query: UserQuery):

    ''' INPUT FORMAT
    query:
    {
        'data': 
        [
            {
                'Year': 'str',
                'Status': 'str',
                'School': 'str',
                'Program': 'str',
                'Average': 'str',
                'Decision Date': 'str'
            }
        ],
        'main': 
        {
            'Year': str,
            'School': str,
            'Program': str
        },
        'filters': 
        {
            'Year': [2024, 2025],
            'School': [str],
            'Program': []
        }
    }
    '''

    ''' OUTPUT FORMAT
    {
        "Description": str,
        "Images": [
            {
                "Image": Base64 Str,
                "Name": str,
                "Description": str
            }
        ],
        "Stats": {
            "Percent Admission": float,
            "Mean": float,
            "Median": float,
            "Max": float,
            "Min": float
        }
    }
    '''

    file_size_limit = 512 * 1024 
    if sys.getsizeof(query.data) + sys.getsizeof(query.filters) + sys.getsizeof(query.data) > file_size_limit:
        raise HTTPException(status_code=413, detail="Data Exceeds 500 KB")

    ret = generate_graphs(query.main_query, query.filters, query.data)
    if ret["Status"] >= 400:
        raise HTTPException(status_code=ret["Status"], detail=ret["Description"])

    return ret["Description"]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
else:
    handler = Mangum(app)


# 1.82s upload benchmark
# 4.26s create graphs

# after speed-ups

# 1.09 upload benchmark
# 1.64 create graphs