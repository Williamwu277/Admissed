from flask import Response
from random import randint

import json


def format_response(info: dict, status: int):

    response = Response(
        response = json.dumps(info),
        status = status,
        mimetype = "application/json"
    )

    response.status_code = status
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


class Server:


    def __init__(self):
        
        self.data = {}

    
    def generate_id(self):

        CAP = 1000000000
        id = randint(1, CAP)

        while id in self.data:
            id = randint(1, CAP)
        
        return id

    
    def upload_spreadsheet(self, link: str):
        pass


    def upload_singular(self, year: int, school: str, program: str, average: float, application: str, decision_date: str):
        
        id = self.generate_id()
        self.data[id] = {
            "id": id,
            "year": year,
            "school": school,
            "program": program,
            "average": average,
            "application": application,
            "decision_date": decision_date
        }

        # probably have to do checks here to determine if the data is valid or not later

        response = self.data[id]
        response["status"] = "success"
        return format_response(response)





