from Const import SCHOOL_NICKNAMES, PROGRAM_NICKNAMES, USE_COLS, ID_THRESHOLD
from random import randint
from datetime import datetime
from calendar import month_name
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import io
import re
import base64

matplotlib.use('agg')


def date_add_year(r):
    
    # depending on how many numerical / alphabetical characters
    # add the year in case its missing 
    s = r["Decision Date"]
    numeric, alphabetical = 0, 0

    if pd.isna(s):
        return pd.NA

    for i in range(len(s)):
        if s[i].isdigit():
            numeric += 1
        elif s[i].isalpha():
            alphabetical += 1
    
    # determine which year to add
    y = r["Year"]
    try:
        dt = pd.to_datetime(s + " " + y, dayfirst=True)

        if dt.month >= 7: 
            y = str(int(y) - 1)
    except:
        pass
    
    if alphabetical == 0 and numeric <= 4:
        s = s + " " + y

    elif alphabetical > 0 and numeric <= 2:
        s = s + " " + y
    
    s = pd.to_datetime(s, errors="coerce", dayfirst=True)
    if pd.isna(s):
        r["Decision Date"] = pd.NA
    else:
        r["Decision Date"] = s.strftime('%d-%m-%Y')
    
    return r


def year_converter(y):

    if pd.isna(y):
        return pd.NA

    # try to convert to a valid year
    try:
        v = int(y.strip())
        assert(1900 <= v <= datetime.now().year)
        return str(v)
    except:
        return pd.NA


def average_converter(a):

    if pd.isna(a):
        return pd.NA

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

    if pd.isna(s):
        return pd.NA

    # one of accepted, deferred, waitlisted or rejected
    s = s.capitalize()
    if s in ["Accepted", "Deferred", "Waitlisted", "Rejected"]:
        return s
    else:
        return pd.NA


def school_converter(s):

    if pd.isna(s):
        return pd.NA
    elif len(s.strip()) == 0:
        return pd.NA

    # try best to convert to known school
    v = s.lower()
    key_order = sorted([(len(nxt), nxt) for nxt in SCHOOL_NICKNAMES.keys()])[::-1]
    for k in key_order:
        if k[1] in v:
            return SCHOOL_NICKNAMES[k[1]]
        
    return pd.NA


def program_converter(s):

    if pd.isna(s):
        return pd.NA
    elif len(s.strip()) == 0:
        return pd.NA

    # try best to convert to known program
    v = s.lower()
    key_order = sorted([(len(nxt), nxt) for nxt in PROGRAM_NICKNAMES.keys()])[::-1]
    for k in key_order:
        if k[1] in v:
            return PROGRAM_NICKNAMES[k[1]]
        
    return pd.NA


def validate_data(data):

    data["Year"] = data["Year"].apply(lambda x: year_converter(x))
    data["Status"] = data["Status"].apply(lambda x: status_converter(x))
    data["School"] = data["School"].apply(lambda x: school_converter(x))
    data["Program"] = data["Program"].apply(lambda x: program_converter(x))
    data["Average"] = data["Average"].apply(lambda x: average_converter(x))
    data = data.apply(date_add_year, axis=1)
    #data["Decision Date"] = pd.to_datetime(data["Decision Date"], errors="coerce").dt.strftime('%Y-%m-%d')

    return data


def upload_data(data, ids):

    all_ids = set(ids)

    # read in data from csv, preprocess it while converting to string
    try:
        data = pd.read_csv(
            data, 
            usecols=USE_COLS, 
            dtype="string"
        )
    except pd.errors.EmptyDataError:
        return {
            "Status": 400,
            "Description": "Data Missing Fields/Columns"
        }
    except pd.errors.ParserError:
        return{
            "Status": 400,
            "Descrption": "Issue with Data Format"
        }
    except ValueError:
        return {
            "Status": 400,
            "Description": "Data Missing Fields/Columns"
        }
    except Exception:
        return {
            "Status": 400,
            "Description": "Issue with Uploaded Data"
        }
    
    # if empty, return empty data
    if data.empty:

        return {
            "Status": 400,
            "Description": "Data Missing Fields/Columns"
        }

    # validate data
    try:
        data = validate_data(data)
    except Exception:
        return {
            "Status": 400,
            "Description": "Error Parsing/Incorrect Data"
        }

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
    return {
        "Status": 200,
        "Description": records
    }


def generate_graphs(query, filters, data):

    try:
        original_table = pd.DataFrame(
            data, 
            columns=["Year", "Status", "School", "Program", "Average", "Decision Date"],
            dtype="string"
        )
    except pd.errors.EmptyDataError:
        return {
            "Status": 400,
            "Description": "Data Missing Fields/Columns"
        }
    except pd.errors.ParserError:
        return{
            "Status": 400,
            "Descrption": "Issue with Data Format"
        }
    except ValueError:
        return {
            "Status": 400,
            "Description": "Data Missing Fields/Columns"
        }
    except Exception:
        return {
            "Status": 400,
            "Description": "Issue with Uploaded Data"
        }
    
    # validate data
    # same steps apply as in the upload function
    try:
        original_table = validate_data(original_table)
    except Exception:
        return {
            "Status": 400,
            "Description": "Error Parsing/Incorrect Data"
        }

    if not ["Program", "School", "Year"] == sorted(query.keys()):
        return {
            "Status": 400,
            "Description": "Issue with Main Query"
        }
    elif not ["Program", "School", "Year"] == sorted(filters.keys()):
        return {
            "Status": 400,
            "Description": "Issue with Secondary Queries"
        }


    # convert decision date back to datetime object
    original_table["Decision Date"] = pd.to_datetime(original_table["Decision Date"], dayfirst=True)

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

    # TODO: Admission average per month

    ret = []
    report_string = ""
    ret.append(generate_admissions_per_month_yearly(pruned_table, filter_years, query))
    ret.append(generate_median_per_month_yearly(pruned_table, filter_years, query))
    ret.append(generate_acceptance_number_by_grade(pruned_table, query))
    
    if len(filter_years) > 1:
        ret.append(generate_acceptance_percent_by_grade_yearly(pruned_table, filter_years, query))
        report_string += (
            "It will also seek to examine the grade-based admission percentage over the year(s) "
            f"{filters["Year"][0] if len(filters["Year"]) == 1 else ", ".join(filters["Year"][:-1]) + " and " + filters["Year"][-1]}. "
        )

    if len(filter_schools) > 1:
        ret.append(generate_school_program_acceptance_rate(pruned_table, filter_schools, query))
        report_string += (
            "In addition, the admission rate by grade for the school(s) "
            f"{filters["School"][0] if len(filters["School"]) == 1 else ", ".join(filters["School"][:-1]) + " and " + filters["School"][-1]}"
            " will be considered too. "
        )

    if len(filter_programs) > 1 or len(filter_years) + len(filter_schools) == 2:
        ret.append(generate_acceptance_percent_multiple_program(pruned_table, filter_programs, query))
        report_string += (
            "Moreover, the grade-wise admission rate will be computed over the program(s) "
            f"{filter_programs[0] if len(filter_programs) == 1 else ", ".join(filter_programs[:-1]) + " and " + filter_programs[-1]}. "
        )

    stat = generate_statistics(pruned_table, query)

    return {
        "Status": 200,
        "Description": {
            "Description": (
                f"This unofficial report will analyze the admission statistics of {query["Program"]} at {query["School"]} in the year {query["Year"]}. "
                "It will calculate the monthly median admission average, monthly admission count, and admission count by grade. "
                f"{report_string}"
                "Finally, it will evaluate the general percentage admission, mean, median, min and max. "
                "Note that since the data could be user-collected, the conclusions reached by this report are "
                "subject to various biases and should be taken with a grain of salt. "
                "A blank report could arise from missing and/or incorrect data."
            ),
            "Images": ret,
            "Stats": stat
        }
    }


def generate_admissions_per_month_yearly(pruned_table, filter_years, query):

    # construct graph for admission count per month by year for a singular program
    fig, ax = plt.subplots(layout='constrained')
    ticks = np.arange(10)
    width = 1 if len(filter_years) == 1 else round(1 / len(filter_years), 1)
    offset = 0
    x_label = []
    description = ""

    for year in sorted(filter_years):

        # prune for a certain school year and the singular program
        df = pruned_table[
            (pruned_table["School"].isin([query["School"]])) &
            (pruned_table["Program"].isin([query["Program"]])) &
            (pd.to_datetime(str(int(year)-1) + " Sept 1", dayfirst=True) < pruned_table["Decision Date"]) &
            (pruned_table["Decision Date"] < pd.to_datetime(year + " July 1", dayfirst=True)) &
            (pruned_table["Status"] == "Accepted")
        ][["Decision Date"]]

        # aggregate to months and count admissions
        df["Admission Count"] = 1
        df = df.groupby(pd.Grouper(key="Decision Date", freq="ME")).agg("sum")
        df = df.reindex(pd.date_range(start=pd.to_datetime(str(int(year)-1) + " Sept 1", dayfirst=True), end=pd.to_datetime(year + " July 1", dayfirst=True), freq="ME"), fill_value=0)
        x_label = months = df["Month"] = df.index.map(lambda x: month_name[x.month])

        # plot on the bar graph
        ax.bar(ticks+offset, height=df["Admission Count"], width=width, label=year)
        offset += width

        if year == query["Year"]:

            counts = df["Admission Count"].tolist()
            mx = sum(counts)
            counts = sorted([(counts[i], months[i]) for i in range(len(counts))])
            main_rounds = []

            for nxt in counts:
                if nxt[0] / max(mx, 1) >= 0.25:
                    main_rounds.append(nxt[1])
            
            if len(main_rounds) > 0:
                description = (
                    f"It seems that the main admission rounds for {query["Program"]} at {query["School"]} are in "
                    f"{main_rounds[0] if len(main_rounds) == 1 else ", ".join(main_rounds[:-1]) + " and " + main_rounds[-1]}. "
                )
            else:
                description = f"It seems that the admissions for {query["Program"]} at {query["School"]} operate on a more spread-out, rolling basis."

    center_offset = 0.25
    ax.set_ylabel("Number of Admissions")
    ax.set_xlabel("Month of School Year")
    ax.set_title(f"{query["Program"]} at {query["School"]}")
    ax.legend()

    x_label = [v[:3] for v in x_label]
    ax.set_xticks(ticks+(center_offset if width != 1 else 0), x_label)

    img_file = io.BytesIO()
    plt.savefig(img_file, format="jpg")
    img_file.seek(0) 
    plt.close()

    return {
        "Image": base64.b64encode(img_file.getvalue()).decode(),
        "Name": f"Monthly Admission Count for {query["Program"]} at {query["School"]}",
        "Description": description
    }


def generate_median_per_month_yearly(pruned_table, filter_years, query):

    # construct graph for average per month by year for a singular program
    fig, ax = plt.subplots(layout='constrained')
    ticks = np.arange(10)
    width = 1 if len(filter_years) == 1 else round(1 / len(filter_years), 1)
    offset = 0
    months = []

    for year in sorted(filter_years):

        # prune for a certain school year and the singular program
        df = pruned_table[
            (pruned_table["School"].isin([query["School"]])) &
            (pruned_table["Program"].isin([query["Program"]])) &
            (pd.to_datetime(str(int(year)-1) + " Sept 1", dayfirst=True) < pruned_table["Decision Date"]) &
            (pruned_table["Decision Date"] < pd.to_datetime(year + " July 1", dayfirst=True)) &
            (pruned_table["Status"] == "Accepted")
        ][["Decision Date", "Average"]]

        # aggregate to months and find median
        df["Average"] = df["Average"].astype(float)
        df = df.groupby(pd.Grouper(key="Decision Date", freq="ME")).agg("median")
        df = df.reindex(pd.date_range(start=pd.to_datetime(str(int(year)-1) + " Sept 1", dayfirst=True), end=pd.to_datetime(year + " July 1", dayfirst=True), freq="ME"), fill_value=0)
        months = df["Month"] = df.index.map(lambda x: month_name[x.month][:3])

        # plot on the bar graph
        ax.bar(ticks+offset, height=df["Average"], width=width, label=year)
        offset += width

    center_offset = 0.25
    ax.set_ylim([65, 105])
    ax.set_ylabel("Median Admission Percentage")
    ax.set_xlabel("Month of School Year")
    ax.set_title(f"{query["Program"]} at {query["School"]}")
    ax.legend()
    ax.set_xticks(ticks+(center_offset if width != 1 else 0), months)

    img_file = io.BytesIO()
    plt.savefig(img_file, format="jpg")
    img_file.seek(0) 
    plt.close()

    return {
        "Image": base64.b64encode(img_file.getvalue()).decode(),
        "Name": f"Monthly Median Admission % for {query["Program"]} at {query["School"]} in {query["Year"]}",
        "Description": (
            "Note that some data points may be skewed due to low sample size. Refer to the previous graph for such points."
        )
    }


def calculate_percentages(s):

    # remove outliers
    if len(s) < 2:
        return np.nan

    v = s.value_counts(normalize=True)
    if "Accepted" in v:
        return round(v["Accepted"] * 100, 1)
    else:
        return 0.0


def generate_acceptance_percent_by_grade_yearly(pruned_table, filter_years, query):

    plt.figure()
    for year in sorted(filter_years):

        # prune for a certain school year and the singular program
        df = pruned_table[
            (pruned_table["School"].isin([query["School"]])) &
            (pruned_table["Program"].isin([query["Program"]])) &
            (pruned_table["Year"] == year)
        ][["Average", "Status"]]

        # aggregate to percentages and calculate % admission
        df["Average"] = df["Average"].astype(float).round()
        df = df.set_index("Average")
        df = df.groupby("Average").agg(
            lambda x: calculate_percentages(x)
        )
        df = df.reindex(range(70, 101))
    
        plt.plot(df.index, df["Status"], label=year)

    plt.ylabel("Percentage of Admission")
    plt.ylim([0, 110])
    plt.xlim([65, 105])
    plt.xlabel("Grade")
    plt.title(f"{query["Program"]} at {query["School"]}")
    plt.legend()

    img_file = io.BytesIO()
    plt.savefig(img_file, format="jpg")
    img_file.seek(0) 
    plt.close()

    return {
        "Image": base64.b64encode(img_file.getvalue()).decode(),
        "Name": f"Acceptance Rate by Grade for {query["Program"]} at {query["School"]}",
        "Description": "Points with too low of a sample size have been omitted from this graph for more clarity."
    }


def count_acceptances(s):

    v = s.value_counts()
    if "Accepted" in v:
        return v["Accepted"]
    else:
        return 0


def generate_acceptance_number_by_grade(pruned_table, query):

    # prune for a certain school year and the singular program
    df = pruned_table[
        (pruned_table["School"].isin([query["School"]])) &
        (pruned_table["Program"].isin([query["Program"]])) &
        (pruned_table["Year"].isin([query["Year"]]))
    ][["Average", "Status"]]

    # aggregate to percentages and calculate % admission
    df["Average"] = df["Average"].astype(float).round()
    df = df.set_index("Average")

    df = df.groupby("Average").agg([
        lambda x: count_acceptances(x),
        lambda x: sum(x.value_counts()) - count_acceptances(x)
    ])
    
    df = df.reindex(range(70, 101), fill_value = 0)
    df.columns = ["Accepted", "Other"]

    fig, ax = plt.subplots()
    
    ax.bar(df.index, df["Accepted"], label="Accepted")
    ax.bar(df.index, df["Other"], label="Other", bottom=df["Accepted"])

    ax.set_ylabel("Verdict Count")
    ax.set_xlabel("Grade")
    ax.set_title(f"{query["Program"]} at {query["School"]}")
    ax.legend()

    img_file = io.BytesIO()
    plt.savefig(img_file, format="jpg")
    img_file.seek(0) 
    plt.close()

    return {
        "Image": base64.b64encode(img_file.getvalue()).decode(),
        "Name": f"Acceptance Verdict by Grade for {query["Program"]} at {query["School"]} in {query["Year"]}",
        "Description": "'Other' includes the summation of the applicants who received a Waitlisted, Deferred or Rejected verdict."
    }


def generate_school_program_acceptance_rate(pruned_table, filter_schools, query):

    plt.figure()
    for school in sorted(filter_schools):

        # prune for a certain school year and the singular program
        df = pruned_table[
            (pruned_table["School"] == school) &
            (pruned_table["Program"] == query["Program"]) &
            (pruned_table["Year"] == query["Year"])
        ][["Average", "Status"]]

        # aggregate to percentages and calculate % admission
        df["Average"] = df["Average"].astype(float).round()
        df = df.set_index("Average")
        df = df.groupby("Average").agg(
            lambda x: calculate_percentages(x)
        )
        df = df.reindex(range(70, 101))
    
        plt.plot(df.index, df["Status"], label=school)

    plt.ylabel("Percentage of Admission")
    plt.ylim([0, 110])
    plt.xlim([65, 105])
    plt.xlabel("Grade")
    plt.title(f"{query["Program"]} in {query["Year"]}")
    plt.legend()
    
    img_file = io.BytesIO()
    plt.savefig(img_file, format="jpg")
    img_file.seek(0) 
    plt.close()

    return {
        "Image": base64.b64encode(img_file.getvalue()).decode(),
        "Name": f"Acceptance Rate by Grade for {query["Program"]} in {query["Year"]}",
        "Description": "Points with too low of a sample size have been omitted from this graph for more clarity."
    }


def generate_acceptance_percent_multiple_program(pruned_table, filter_programs, query):

    plt.figure()
    for program in sorted(filter_programs):

        # prune for a certain school year and the singular program
        df = pruned_table[
            (pruned_table["School"] == query["School"]) &
            (pruned_table["Program"] == program) &
            (pruned_table["Year"] == query["Year"])
        ][["Average", "Status"]]

        # aggregate to percentages and calculate % admission
        df["Average"] = df["Average"].astype(float).round()
        df = df.set_index("Average")
        df = df.groupby("Average").agg(
            lambda x: calculate_percentages(x)
        )
        df = df.reindex(range(70, 101))
    
        plt.plot(df.index, df["Status"], label=program)

    plt.ylabel("Percentage of Admission")
    plt.ylim([0, 110])
    plt.xlim([65, 105])
    plt.xlabel("Grade")
    plt.title(f"{query["School"]} in {query["Year"]}")
    plt.legend()
    
    img_file = io.BytesIO()
    plt.savefig(img_file, format="jpg")
    img_file.seek(0) 
    plt.close()

    return {
        "Image": base64.b64encode(img_file.getvalue()).decode(),
        "Name": f"Acceptance Rate by Grade for {query["School"]} in {query["Year"]}",
        "Description": "Points with too low of a sample size have been omitted from this graph for more clarity."
    }


def generate_statistics(pruned_table, query):

    # TODO: if blank graph, these return NAN which results in error

    df = pruned_table[
        (pruned_table["Year"] == query["Year"]) &
        (pruned_table["School"] == query["School"]) & 
        (pruned_table["Program"] == query["Program"])
    ]

    df["Average"] = df["Average"].astype(float)
    v = df["Status"].value_counts(normalize=True)

    mean = df["Average"].mean()
    median = df["Average"].median()
    mx = df[df["Status"] == "Accepted"]["Average"].max()
    mn = df[df["Status"] == "Accepted"]["Average"].min()

    stat = {
        "Percent Admission": round(v["Accepted"] * 100, 1) if "Accepted" in v else 0.0,
        "Mean": "N/A" if pd.isna(mean) else round(mean, 1),
        "Median": "N/A" if pd.isna(median) else round(median, 1),
        "Max": "N/A" if pd.isna(mx) else round(mx, 1),
        "Min": "N/A" if pd.isna(mn) else round(mn, 1)
    }

    return stat