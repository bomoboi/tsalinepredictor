#!/usr/bin/env python3
import camelot
import datetime as dt
import httpx
import pandas as pd
import re
import os
import time
from bs4 import BeautifulSoup
from sqlalchemy import text, Table, Column, Integer, String
from tqdm import tqdm
from uuid import uuid4

pd.set_option('mode.chained_assignment', None)

DATE_REG = re.compile(r"^([1-9]|1[0-2])\/([1-9]|[12][0-9]|3[0-1])\/(20(?:1[7-9]|2[0-4]))$")
HOUR_REG = re.compile(r"^(0[0-9]|1[0-9]|2[0-3]):00$")
CODE_REG = re.compile(r"^([A-Z]{3})$")
AP_REG = re.compile(r"^(^[a-zA-Z .'-]+$)$")
CHK_REG = re.compile(r"^(^[a-zA-Z0-9 .'-]+$)$")
# creds to https://stackoverflow.com/a/53823071
PMIS_REG = re.compile(r"^[+-]?([0-9]{1,3}(,[0-9]{3})*(\.[0-9]+)?|\d*\.\d+|\d+)$")



def parse_pdf(fp: str,
              page_range: str="all",
              line_tol: int=80):
    # this is just to measure the time it takes to read a pdf
    pdf_time = time.time()
    # reads the pdf, outputs a wrapper for a pandas df
    tables = camelot.read_pdf(filepath=fp,
                              pages=page_range,
                              strip_text="\n",
                              line_scale=line_tol,
                              split_text=False,
                              copy_text="v",
                              line_tol=5,
                              joint_tol=3,
                              iterations=4,
                              threshold_blocksize=3)

    print(f"PDF processed in {(time.time() - pdf_time)/60} m ({time.time() - pdf_time} s)")

    # instead do
    concat_time = time.time()
    df_final = pd.concat([ parse_df(t.df, fp) for t in tqdm(tables) ], ignore_index=True)
    print(f"Finished concatenating in {(time.time() - concat_time)/60} m ({time.time() - concat_time} s")
    return df_final

# gets the correct columns from the dataframe
def parse_df(df, fp):


    # Trims columns and rows that are entirely empty
    df.replace("", None, inplace=True)
    df.dropna(how="all", axis=1, inplace=True)
    df.dropna(how="all", axis=0, inplace=True)

    # quad time loop until you get the first valid date match

    df_iter = df.iterrows()
    index_tuple = (0, 0)

    for i, r in enumerate(df_iter):
        if index_tuple == (0, 0):
            for i2, s in enumerate(r[1]):
                s = str(s).strip()
                if pd.isna(s):
                    continue
                elif DATE_REG.fullmatch(s) != None:
                    month = int(DATE_REG.fullmatch(s).group(1))
                    day = int(DATE_REG.fullmatch(s).group(2))
                    year = int(DATE_REG.fullmatch(s).group(3))

                    df_date = dt.date(day = day,
                                    month = month,
                                    year = year)

                    date_string = fp.split("/")[-1].split(".")[0]
                    d_start = dt.datetime.strptime(date_string[:6], "%m%d%y").date()
                    d_end = dt.datetime.strptime(date_string[7:], "%m%d%y").date()

                    if d_start <= df_date <= d_end:
                        index_tuple = (i, i2)
                        break
                    else:
                        continue
        else:
            break

    # then strip off all extraneous cols and rows

    df.drop(columns = range(index_tuple[0]),
            index = range(index_tuple[1]),
            inplace=True)
    df.columns = [c for c in range(len(df.columns))]


    # now do the same loop but we're checking for the first valid row
    df_iter = df.iterrows()

    data_cols = {"date": 0,
                 "hour": None,
                 "code": None,
                 "chk": None,
                 "PMIS": None}

    for ir, r in df_iter:
        for i, f in enumerate(r):
            if f == None:
                 continue
            # test for hour
            elif HOUR_REG.fullmatch(f) != None:
                data_cols["hour"] = i
                continue

            # test for IATA code
            elif CODE_REG.fullmatch(f) != None:
                data_cols["code"] = i
                continue

            # if we're looping and we encounter something that matches checkpoint
            # for the first time, that also matches airport, check to see if
            # there's another value that matches checkpoint, as the actual checkpoint
            # will always be the last thing to match checkpont
            #

            elif CHK_REG.fullmatch(f) != None and data_cols["chk"] == None:
                #stat1 = CHK_REG.fullmatch(f)
                #stat2 = AP_REG.fullmatch(f)
                #print(f"{stat1} {stat2}")
                if AP_REG.fullmatch(f) != None:
                    for i2, f2 in enumerate(r[i+1:]):
                        if CHK_REG.fullmatch(str(f2)) != None:
                            data_cols["chk"] = i+i2
                            continue
                        else:
                            data_cols["chk"] = i
                            continue
                else:
                    data_cols["chk"] = i
                    continue



            #test for PMIS
            elif PMIS_REG.fullmatch(f) != None:
                data_cols["PMIS"] = i
                continue

        #print(data_cols)
        if None in data_cols.values():
            # if any of the values haven't been assigned, then this isn't a valid row
            # and we can't get the columns we need from it
            data_cols = {"date": 0,
                         "hour": None,
                         "code": None,
                         "chk": None,
                         "PMIS": None}

            df.drop(index=ir, inplace=True)
        else:
            break


    df = df[data_cols.values()]
    df.columns = ["Date", "Hour", "Code", "Checkpoint", "PMIS"]
    df.dropna(how="all", axis=1, inplace=True)
    df.dropna(how="all", axis=0, inplace=True)
    df.reindex()

    return df


# adds a row to the database
def add_record(index, row, engine, metadata):

    # accessing data from the tuple
    date = row[0]
    # formatting date according to ISO 8601
    date = dt.datetime.strptime(date, "%m/%d/%Y").date().isoformat()

    hour = int(row[1].split(":")[0])
    code = str(row[2])

    if row[3] == None:
        chk = f"{index}-{uuid4().hex}"
    else:
        chk = str(row[3]).strip()
        chk = re.sub(r'[^a-zA-Z0-9\n\.]', " ", chk)
        chk = re.sub(" ", "_", chk)

    pmis = int("".join(row[4].split(',')))

    # checking to see if the airport is already in the database, adding it if not
    if f"{code}_tbl" in metadata.tables.keys():
        # selecting the correct airport if it exists
        tbl = Table(f"{code}_tbl", metadata, autoload_with=engine)
        rtrn = None
    else:
        #print(f"Creating new table {code}")
        tbl = Table(f"{code}_tbl",
                metadata,
                Column('day', String(12), primary_key=True),
                Column('hour', Integer, primary_key=True),
                Column('checkpoint', String(64), primary_key=True),
                Column('travelers', Integer),
                quote=False)
        tbl.create(bind=engine)
        rtrn = code


    # adding the data to the correct airport
    with engine.connect() as conn:
        # there exists a more pythonic way to do this but i could not make it work
        conn.execute(text(f'INSERT INTO {code}_tbl (day, hour, checkpoint, travelers) VALUES ("{date}", {hour}, "{chk}", {pmis})'))
        conn.commit()

    return rtrn


def send_df(dataframe, engine, metadata):

    # creds to https://stackoverflow.com/a/77270285, this used to be a for loop that
    # took 5x the time to run
    # this runs add_record for every row in the dataframe
    out = [
        add_record(i, r, engine, metadata) for i, r in tqdm(enumerate(zip(dataframe["Date"],
                                                  dataframe["Hour"],
                                                  dataframe["Code"],
                                                  dataframe["Checkpoint"],
                                                  dataframe["PMIS"])))
    ]

    #the length of out == number of records processed
    num_records = len(out)
    out = pd.Series(out)
    #gets rid of all the None values, leaving a list of all the airports created
    out.dropna(inplace=True)

    #make sure all our changes are committed
    metadata.create_all(bind=engine)

    return out, num_records, dataframe.iloc[-1]["Date"]

def download_pdf(page):

    SITE_REGEX = re.compile(r'\/sites\/default\/files\/foia-readingroom\/(.*).pdf')

    links = {}
    for p in range(page):
        rq = f"https://www.tsa.gov/foia/readingroom?title=TSA%20Throughput&field_foia_category_value=Airport&page={p}"
        page = httpx.get(rq)
        for link in BeautifulSoup(page.content,
                                  features="html.parser").find_all("a"):
            if link.has_attr("href"):
                href = link.get("href")
                if SITE_REGEX.search(href):
                    #print(f"Found pdf {href}")
                    date_array = []
                    for w in link.contents[0].split(" "):
                        w = w.replace(",", "")
                        if not w:
                            continue
                        if w[0].lower() in ["a", "d", "f", "j", "m", "n", "o", "s"] and w.lower() != "data":
                            date_array.append(w)
                        else:
                            try:
                                #print(w)
                                date_array.append(str(int(w)))
                            except ValueError:
                                pass

                    #print(date_array)
                    #print("".join(date_array[0:3]))
                    date_start = dt.datetime.strptime("".join(date_array[0:3]),
                                                     "%B%d%Y")
                    date_end = dt.datetime.strptime("".join(date_array[3:]),
                                                    "%B%d%Y")
                    date_start = date_start.strftime("%Y-%m%d")
                    date_end = date_end.strftime("%m%d")

                    date_string = f"{date_start}{date_end}"

                    links[date_string] = href.split(".")[0]


    for u in links.items():
        byte_pdf = httpx.get(f"https://www.tsa.gov{u[1]}.pdf").content

        indir = __file__.split("/")[1:-2]
        indir = "/".join(indir)
        INPUT_DIR = f"/{indir}/input"

        # check that input has RWX
        if not (os.access(INPUT_DIR, mode=os.R_OK+os.W_OK+os.X_OK)):
            raise PermissionError(f"Couldn't access {INPUT_DIR}")

        with open(f"{INPUT_DIR}/{u[0]}.pdf", "wb") as pdf:
            pdf.write(byte_pdf)
        print(f"Wrote {u[0]}.pdf")
