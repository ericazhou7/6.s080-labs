SELECT
        CANDIDATE.CAND_NAME,
        CAND_PTY_AFFILIATION,
        TTL_INDIV_CONTRIB,
        TTL_RECEIPTS,
        TTL_INDIV_CONTRIB/TTL_RECEIPTS as RATIO_INDIV
    FROM
        CANDIDATE
    JOIN
        CAND_SUMMARY
            ON CANDIDATE.CAND_ID = CAND_SUMMARY.CAND_ID
    WHERE
        CAND_OFFICE = 'H'
        AND CAND_STATUS IN ('C', 'N')
        AND CAND_ELECTION_YR = 2016
        AND TTL_RECEIPTS > 100000
    ORDER BY
        RATIO_INDIV
    LIMIT 10;
