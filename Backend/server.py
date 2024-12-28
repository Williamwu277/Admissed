from Const import SCHOOL_NICKNAMES, PROGRAM_NICKNAMES, USE_COLS, ID_THRESHOLD
from random import randint
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import re

matplotlib.use('agg')


def date_add_year(r):

    # depending on how many numerical / alphabetical characters
    # add the year in case its missing 
    s = r["Decision Date"]
    numeric, alphabetical = 0, 0

    for i in range(len(s)):
        if s[i].isdigit():
            numeric += 1
        elif s[i].isalpha():
            alphabetical += 1
    
    if alphabetical == 0 and numeric <= 4:
        r["Decision Date"] = s + " " + r["Year"]
    elif alphabetical > 0 and numeric <= 2:
        r["Decision Date"] = s + " " + r["Year"]
    
    return r


def year_converter(y):

    # try to convert to a valid year
    try:
        v = int(y)
        assert(1900 <= v <= datetime.now().year)
        return str(v)
    except:
        return pd.NA


def average_converter(a):

    # try to convert to a valid percentage
    a = re.sub(r"[^0-9.]", "", a)

    try:
        v = float(a)
        v = round(v, 1)
        assert(0 <= v <= 100)
        return str(v)
    except: 
        return pd.NA


def status_converter(s):

    # one of accepted, deferred, waitlisted or rejected
    s = s.capitalize()
    if s in ["Accepted", "Deferred", "Waitlisted", "Rejected"]:
        return s
    else:
        return pd.NA


def school_converter(s):

    # try best to convert to known school
    v = s.lower()
    for k in SCHOOL_NICKNAMES:
        if k in v:
            return SCHOOL_NICKNAMES[k]
        
    return s


def program_converter(s):

    # try best to convert to known program
    v = s.lower()
    for k in PROGRAM_NICKNAMES:
        if k in v:
            return PROGRAM_NICKNAMES[k]
        
    return s


def validate_data(data):

    data["Year"] = data["Year"].apply(lambda x: year_converter(x))
    data["Status"] = data["Status"].apply(lambda x: status_converter(x))
    data["School"] = data["School"].apply(lambda x: school_converter(x))
    data["Program"] = data["Program"].apply(lambda x: program_converter(x))
    data["Average"] = data["Average"].apply(lambda x: average_converter(x))
    data = data.apply(date_add_year, axis=1)
    data["Decision Date"] = pd.to_datetime(data["Decision Date"], errors="coerce").dt.strftime('%Y-%m-%d')

    return data


def upload_data(data, ids):

    all_ids = set(ids)

    # read in data from csv, preprocess it while converting to string
    data = pd.read_csv(
        data, 
        usecols=USE_COLS, 
        dtype="string"
    )

    # validate data
    data = validate_data(data)

    # preprocess dates without years
    # if there is no month or date, return NA
    data = data.apply(date_add_year, axis=1)

    # convert decision dates to datetime format
    data["Decision Date"] = pd.to_datetime(data["Decision Date"], errors="coerce").dt.strftime('%Y-%m-%d')

    # create id column
    ids = []
    for _ in range(len(data)):

        new_id = randint(1, ID_THRESHOLD)
        while new_id in all_ids:
            new_id = randint(1, ID_THRESHOLD)
        ids.append(str(new_id))

    data["id"] = ids

    # add error flags
    data["Flag"] = data.apply(
        lambda row: "Y" if row.isna().any() else "N",
        axis=1
    )

    # front-end cannot render NA, convert to string
    data = data.fillna("")

    # decision date and average back to string
    data["Decision Date"] = data["Decision Date"].astype(str)

    records = data.to_dict('records')
    return records


def generate_graphs(query, filters, data):

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

    # TODO error checking for this function

    original_table = pd.DataFrame(
        data, 
        columns=["Year", "Status", "School", "Program", "Average", "Decision Date"],
        dtype="string"
    )
    
    # validate data
    # same steps apply as in the upload function
    original_table = validate_data(original_table)

    # kill rows with NA
    original_table = original_table.dropna()

    # Prune data with filters and query
    filter_years = [query["Year"]] + filters["Year"]
    filter_schools = [query["School"]] + filters["School"]
    filter_programs = [query["Program"]] + filters["Program"]

    pruned_table = original_table[
        original_table["Year"].isin(filter_years) &
        original_table["School"].isin(filter_schools) &
        original_table["Program"].isin(filter_programs)

    ]

    # Group by singular program

    print(pruned_table.head())
    
    return 1

