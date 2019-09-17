import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sqlite3 as sql
import pandas as pd
import argparse

def runSQL(query_num):
    with sql.connect("lab1.sqlite") as conn, open("queries/q{}.sql".format(query_num)) as in_query:
        cur = conn.cursor()
        df = pd.read_sql_query(in_query.read(), conn)
        return df

def Q1Pandas():
    df = pd.read_csv("data/candidate.txt",delimiter = "|")
    status_mask = df['CAND_STATUS'].isin(['C','N'])
    year_mask = df['CAND_ELECTION_YR'] == 2016
    office_mask = df['CAND_OFFICE'] == "P"
    mask = status_mask & year_mask & office_mask
    return pd.DataFrame([df[mask]['CAND_NAME'].count()])

def Q2Pandas():
    df = pd.read_csv("data/candidate.txt",delimiter = "|")
    status_mask = df['CAND_STATUS'].isin(['C','N'])
    year_mask = df['CAND_ELECTION_YR'] == 2016
    office_mask =  df['CAND_OFFICE'] == "S"
    mask = status_mask & year_mask & office_mask
    df = df[mask]

    third_party_mask = ~df['CAND_PTY_AFFILIATION'].isin(['REP','IND','DEM'])
    counts = df[third_party_mask].groupby('CAND_PTY_AFFILIATION')['CAND_ID'].count()
    return counts.sort_values(ascending=False)

def Q3Pandas():
    df = pd.read_csv("data/pac_summary.txt",delimiter="|")
    df = df[df['CMTE_TP']=='O']
    return df[['CMTE_NM','TTL_RECEIPTS']].sort_values('TTL_RECEIPTS', ascending = False)[:10]

def Q4Pandas():
    """
    TODO: Write your Pandas query here, return a dataframe to answer the question
    """
    return None

def Q5Pandas():
    """
    TODO: Write your Pandas query here, return a dataframe to answer the question
    """
    return None

def Q6Pandas():
    """
    TODO: Write your Pandas query here, return a dataframe to answer the question
    """
    return None

def Q7Pandas():
    """
    TODO: Write your Pandas query here, return a dataframe to answer the question
    """
    return None

pandas_queries = [Q1Pandas, Q2Pandas, Q3Pandas, Q4Pandas, Q5Pandas, Q6Pandas, Q7Pandas]
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", "-q", help="Run a specific query", type=int)
    args = parser.parse_args()

    queries = range(1, 12)
    if args.query != None:
        queries = [args.query]
    for query in queries:
        print("\nQuery {}".format(query))
        if query <= 7:
            print("\nPandas Output")
            print(pandas_queries[query-1]())
        print("\nSQLite Output")
        print(runSQL(query))
