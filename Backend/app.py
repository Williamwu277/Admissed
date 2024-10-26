from flask import Flask, request
from flask_cors import CORS
from server import Server
import json


app = Flask(__name__)
CORS(app)
server = Server()


if __name__ == "__main__":
    app.run()


@app.route("/api/upload_spreadsheet", methods=["POST"])
def upload_spreadsheet():
    """
    Upload all the data from a spreadsheet to the server.

    Request:
    {
        "link": "https://www.google.com"
    }

    Response:
    {
        "status": "success"
    }
    """
    link = request.form.get("link")

    return server.upload_item(link)


@app.route("api/upload_singular", methods=["POST"])
def upload_singular():
    """
    Upload the data for a singular person to the server.

    Request:
    {
        "year": "2024",
        "school": "University of Waterloo",
        "program": "Computer Science",
        "average": "94",
        "application": "CS Club President",
        "decision_date": "05/02/2022"
    }

    Response:
    {
        "status": "success"
    }
    """

    year = int(request.form.get("year"))
    school = request.form.get("school")
    program = request.form.get("program")
    average = float(request.form.get("average"))
    application = request.form.get("application")
    decision_date = request.form.get("decision_date")

    return server.upload_singular(year, school, program, average, application, decision_date)
