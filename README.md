# AdmissEd
An admission statistics web app. User-collected admissions data is hard for the human-eye to process — to combat this, upload it to AdmissEd and view your data in the format of graphs and statistics. Mobile support exists, so check out the website on your phone too. 🌎 **Sample data can be found in Sample.csv**. Try it live at [admissed.com](https://admissed.com)!

## Table of Contents
1. [About](#about)
2. [Usage](#usage)
3. [Installation](#installation)
4. [Deployment](#deployment)

## About

#### Technologies
* React web application styled with CSS
* Python FastAPI backend
* Pandas and Matplotlib for data analysis
* Hosted using AWS S3, CloudFront, Route 53 and Lambda

## Usage
1. Acquire a spreadsheet containing Ontario admission statistics (self-collected data can be found on the Ontario G12 Reddit by searching for yearly admission spreadsheets)
   * If not, use the sample CSV file in this Github repository
2. Make a copy of the spreadsheet and ensure that the column headings `Year`, `Status`, `School`, `Program`, `Average` and `Decision Date` exist
   * Column headings are case-sensitive
   * `Status` should be one of accepted, rejected, deferred or waitlisted
   * `Decision Date` should be in day, month then year format
3. Download the spreadsheet as a CSV file (make sure it is less than 500 KB)
4. Upload it onto AdmissEd
5. View your data on the `view` page
   * Rows may be red if there are invalid inputs
   * AdmissEd will try to sanitize the input to be understandable
6. Choose a main year, school, and program along with secondary fields to generate a report
7. Enjoy~

## Installation

Instructions for running AdmissEd locally:

1. Go into the frontend with `cd Frontend`
3. Run `npm install` for dependencies
4. `npm start` to start the frontend

Then, to start the backend:

1. Go into the backend with `cd Backend`
2. Use a virtual environment `python3 -m venv env`
3. Install requirements using `pip3 install -r requirements.txt`
4. Then, use the virtual environment with `source env/bin/activate`
5. Finally, call `python3 main.py` to finish

Notes:

* Locally the backend runs on `http://0.0.0.0:8000/`
* You will need to create an image folder in `/Frontend/src/` and populate it with various images to be used (error messages should specify)

## Deployment

TBD
