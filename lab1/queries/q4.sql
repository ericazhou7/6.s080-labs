SELECT
        CAND_NAME,
        CMTE_NM,
        CMTE_ST1
    FROM
        CANDIDATE
    JOIN
        COMMITTEE
            ON CAND_PCC = CMTE_ID
    WHERE
        CAND_OFFICE = 'P'
        AND CAND_STATUS IN ('C', 'N')
        AND CAND_ELECTION_YR = 2016
        AND CAND_NAME LIKE '%HUCK%';
