SELECT
          CAND_PTY_AFFILIATION,
          SUM(TTL_INDIV_CONTRIB),
          SUM(TTL_RECEIPTS),
          SUM(TTL_INDIV_CONTRIB)/SUM(TTL_RECEIPTS) as RATIO_INDIV
  FROM
          CANDIDATE join CAND_SUMMARY on candidate.cand_id = cand_summary.cand_id
  WHERE CAND_OFFICE = 'S'
  AND CAND_STATUS IN ('C', 'N')
  AND CAND_ELECTION_YR = 2016
  GROUP BY 1
  ORDER BY
          RATIO_INDIV desc
  LIMIT 10;
