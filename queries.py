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
    df = pd.read_csv("data/candidate.txt", delimiter = "|")
    status_mask = df['CAND_STATUS'].isin(['C','N'])
    year_mask = df['CAND_ELECTION_YR'] == 2016
    office_mask = df['CAND_OFFICE'] == "P"
    mask = status_mask & year_mask & office_mask
    return pd.DataFrame([df[mask]['CAND_NAME'].count()])

def Q2Pandas():
    df = pd.read_csv("data/candidate.txt", delimiter = "|")
    status_mask = df['CAND_STATUS'].isin(['C','N'])
    year_mask = df['CAND_ELECTION_YR'] == 2016
    office_mask =  df['CAND_OFFICE'] == "S"
    mask = status_mask & year_mask & office_mask
    df = df[mask]

    third_party_mask = ~df['CAND_PTY_AFFILIATION'].isin(['REP','IND','DEM'])
    counts = df[third_party_mask].groupby('CAND_PTY_AFFILIATION')['CAND_ID'].count()
    return counts.sort_values(ascending=False)

def Q3Pandas():
    df = pd.read_csv("data/pac_summary.txt", delimiter="|")
    df = df[df['CMTE_TP']=='O']
    return df[['CMTE_NM','TTL_RECEIPTS']].sort_values('TTL_RECEIPTS', ascending = False)[:10]

def Q4Pandas():
    df = pd.read_csv("data/candidate.txt", delimiter = "|")
    status_mask = df['CAND_STATUS'].isin(['C','N'])
    year_mask = df['CAND_ELECTION_YR'] == 2016
    office_mask = df['CAND_OFFICE'] == "P"
    mask = status_mask & year_mask & office_mask
    pres_candidates = df[mask]
    huck_candidates = pres_candidates[pres_candidates['CAND_NAME'].str.contains('HUCK')]

    committees = pd.read_csv("data/committee.txt", delimiter="|")
    joined = pd.merge(huck_candidates, committees, left_on = 'CAND_PCC', right_on = 'CMTE_ID')[['CAND_NAME','CMTE_NM','CMTE_ST1']]
    return joined

def Q5Pandas():
    df = pd.read_csv("data/candidate.txt", delimiter = "|")
    status_mask = df['CAND_STATUS'].isin(['C','N'])
    year_mask = df['CAND_ELECTION_YR'] == 2016
    office_mask = df['CAND_OFFICE'] == "S"
    mask = status_mask & year_mask & office_mask
    senate_candidates = df[mask]

    committees = pd.read_csv("data/committee.txt", delimiter = "|")
    joined = pd.merge(senate_candidates, committees, left_on = 'CAND_PCC', right_on = 'CMTE_ID')[['CAND_ID_x','CMTE_NM','CMTE_ST']]
    joined.columns = ['CAND_ID','CMTE_NM','CMTE_ST']

    receipts = pd.read_csv("data/cand_summary.txt", delimiter = "|")
    committees_with_receipts = pd.merge(joined, receipts)[['CMTE_NM','CMTE_ST','TTL_RECEIPTS']]

    populations = pd.read_csv("data/dist_pop.txt", delimiter = "|")
    state_pops = populations.groupby('state').sum().reset_index()[['state','population']]
    committees_with_pops = pd.merge(committees_with_receipts, state_pops, left_on = 'CMTE_ST', right_on = 'state')
    committees_with_pops['RECEIPTS_PER_CAPITA'] = committees_with_pops['TTL_RECEIPTS']/committees_with_pops['population']
    return committees_with_pops.sort_values('RECEIPTS_PER_CAPITA',ascending=False)[['CMTE_NM','CMTE_ST','TTL_RECEIPTS','RECEIPTS_PER_CAPITA']]

def Q6Pandas():
    df = pd.read_csv("data/candidate.txt", delimiter = "|")
    status_mask = df['CAND_STATUS'].isin(['C','N'])
    year_mask = df['CAND_ELECTION_YR'] == 2016
    office_mask = df['CAND_OFFICE'] == "H"
    mask = status_mask & year_mask & office_mask
    house_candidates = df[mask][['CAND_NAME','CAND_PTY_AFFILIATION','CAND_ID']]

    receipts = pd.read_csv("data/cand_summary.txt", delimiter = "|")
    candidates_with_receipts = pd.merge(house_candidates, receipts)[['CAND_NAME','CAND_PTY_AFFILIATION','TTL_INDIV_CONTRIB','TTL_RECEIPTS']]
    candidates_with_receipts = candidates_with_receipts[candidates_with_receipts['TTL_RECEIPTS'] > 100000]
    candidates_with_receipts['RATIO_INDIV'] = candidates_with_receipts['TTL_INDIV_CONTRIB']/candidates_with_receipts['TTL_RECEIPTS']
    return candidates_with_receipts.sort_values('RATIO_INDIV')[:10]

def Q7Pandas():
    df = pd.read_csv("data/candidate.txt", delimiter = "|")
    status_mask = df['CAND_STATUS'].isin(['C','N'])
    year_mask = df['CAND_ELECTION_YR'] == 2016
    office_mask = df['CAND_OFFICE'] == "S"
    mask = status_mask & year_mask & office_mask
    senate_candidates = df[mask][['CAND_NAME','CAND_PTY_AFFILIATION','CAND_ID']]

    receipts = pd.read_csv("data/cand_summary.txt", delimiter = "|")
    candidates_with_receipts = pd.merge(senate_candidates, receipts)[['CAND_NAME','CAND_PTY_AFFILIATION','TTL_INDIV_CONTRIB','TTL_RECEIPTS']]
    parties_with_receipts = candidates_with_receipts.groupby('CAND_PTY_AFFILIATION').sum()
    parties_with_receipts['RATIO_INDIV'] = parties_with_receipts['TTL_INDIV_CONTRIB']/parties_with_receipts['TTL_RECEIPTS']
    return parties_with_receipts.sort_values('RATIO_INDIV',ascending=False)[:10]

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
