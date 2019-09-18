SELECT
        COUNT(CAND_ID)
    FROM
        CANDIDATE
    WHERE
        CAND_OFFICE = 'P'
        AND CAND_STATUS IN ('C', 'N')           
        AND CAND_ELECTION_YR = 2016;
