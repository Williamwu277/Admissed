from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from server import upload_data, generate_graphs
from typing import List, Dict, Any
from pydantic import BaseModel
import uvicorn
import json


app = FastAPI()

# TODO: Figure out proper headers to allow

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
    
    # TODO: Santitization 
    # * limit file size
    # * check file type
    
    return upload_data(data.file, ids)


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
    * Marks: mean median range min max
    * Decision Date: earliest, latest, median
    * Graphs
       * Yearly % acceptance by grade (single program, single school)
       * Yearly # acceptance by date (single program, single school)
       * School based % acceptance (single program, multiple school)
       * Program based % acceptance (multiple program, single school)
           * # of values considered etc
    '''

    #print(query)

    return generate_graphs(query.main_query, query.filters, query.data)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)