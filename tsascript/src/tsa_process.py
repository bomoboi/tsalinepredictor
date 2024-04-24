#!/usr/bin/env python3
import argparse
import os
import sys
import time
import tsa_lib as tl
from pandas import read_parquet
from sqlalchemy import create_engine, MetaData


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--parquet",
                        action='store_true',
                        default=False)

    # get a list of files with extension .pdf
    BASE_DIR = __file__.split('/')[1:-2]
    BASE_DIR = f"/{'/'.join(BASE_DIR)}"
    INPUT_DIR = f"/{BASE_DIR}/input"
    OUTPUT_DIR = f"/{BASE_DIR}/output"

    if not (os.access(INPUT_DIR, mode=os.R_OK+os.X_OK)):
        raise PermissionError(f"Couldn't access {INPUT_DIR}")

    if not (os.access(OUTPUT_DIR, mode=os.R_OK+os.X_OK+os.W_OK)):
        raise PermissionError(f"Couldn't access {OUTPUT_DIR}")
    #TODO make this work lol
    #db_engine = create_engine(str(os.getenv("DB_URI")))
    db_engine = create_engine("mariadb+pymysql://tsas_user:FbvD8MxQMQwxJvXwPzClA8U+cgMcmvSnHhRjJPSah74=@10.0.1.1:3306/tsa_data?charset=utf8mb4")
    tsa_db = MetaData()
    tsa_db.reflect(db_engine)

    indir_list = os.listdir(INPUT_DIR)
    indir_list.sort(reverse=True)

    for i, pdf in enumerate(indir_list):

       start_time = time.time()
       print(f"Starting file {pdf} ({i+1}/{len(indir_list)})")
       # send a notif here with pdf name and time
       if pdf.split(".")[-1] != "pdf" or pdf == "":
          #TODO log non pdf file w name and time
          continue

       #TODO make this a match for cli kwarg
       #     only run parse if a parquet file
       #     isn't passed
       if parser.parse_args().parquet:
           parquet_fp = f"/{OUTPUT_DIR}/{pdf.split('.')[0]}.parquet"
           pdf_df = read_parquet(parquet_fp)
       else:
           pdf_df = tl.parse_pdf(f"{INPUT_DIR}/{pdf}")
       #TODO Send a notif that pdf is done

       with open(f"{OUTPUT_DIR}/{pdf[:-4]}.parquet", "wb") as save_file:
          pdf_df.to_parquet(path=save_file,
                            compression="snappy")
       #TODO Send a notif that df has been saved to disk with name and time

       tl.send_df(dataframe = pdf_df,
                  engine = db_engine,
                  metadata = tsa_db)
       print(f"\nFinished pdf {pdf} ({i+1}/{len(indir_list)} in {(time.time()-start_time)/60} m ({time.time()-start_time} s)\n")
       os.rename(src=f"{INPUT_DIR}/{pdf}",
                 dst=f"{BASE_DIR}/processed/{pdf}")

       indir_list = os.listdir(INPUT_DIR)
       indir_list.sort(reverse=True)
