SELECT
        CMTE_NM,
        CMTE_ST,
        TTL_RECEIPTS,
        TTL_RECEIPTS/STATE_POP as RECEIPTS_PER_CAPITA
    FROM
        CANDIDATE,
        CAND_SUMMARY,
        COMMITTEE,
        (
          SELECT
              STATE,
              SUM(POPULATION) AS STATE_POP
          FROM
              DIST_POP
          GROUP BY 1
        )
    WHERE
        CAND_PCC = CMTE_ID
        AND CANDIDATE.CAND_ID = CAND_SUMMARY.CAND_ID
        AND CMTE_ST = STATE
        AND CAND_OFFICE = 'S'
        AND CAND_STATUS IN ('C', 'N')
        AND CAND_ELECTION_YR = 2016
    ORDER BY
        RECEIPTS_PER_CAPITA DESC
    LIMIT 20;
