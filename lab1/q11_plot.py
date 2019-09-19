import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sqlite3 as sql
import pandas as pd
import argparse

def runAndPlotSQL():
    with sql.connect("lab1.sqlite") as conn:
        df = pd.read_sql_query("""
            SELECT
              CAND_NAME,
              SUM(TRANSACTION_AMT) AS TOTAL_IND_CONTRIBUTIONS,
              COUNT(*) AS TOTAL_IND_CONTRIBUTORS,
              SUM(TRANSACTION_AMT)/COUNT(*) AS CONTRIBUTION_PER_DONOR
            FROM
              INDIV_CONTRIB,
              CANDIDATE
            WHERE
              CAND_OFFICE = 'P'
              AND CAND_STATUS IN ('C', 'N')
              AND CAND_ELECTION_YR = 2016
              AND CAND_PCC = CMTE_ID
              AND ENTITY_TP = "IND"
            GROUP BY
              CAND_NAME
            ORDER BY
              TOTAL_IND_CONTRIBUTORS DESC
            LIMIT 10;
            """, conn)
    print(df)
    df.set_index('CAND_NAME').plot.bar(y='CONTRIBUTION_PER_DONOR')
    plt.title('2016 Presidential Race Contributions Per Donor\n(Top 10 by # Contributors)')
    plt.ylabel('Contribution per Donor')
    plt.savefig("q11.png",bbox_inches='tight')

if __name__ == "__main__":
    runAndPlotSQL();
