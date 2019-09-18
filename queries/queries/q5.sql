SELECT
          cmte_nm,
          cmte_st,
          TTL_RECEIPTS,
          ttl_receipts/state_pop as RECEIPTS_PER_CAPITA
  FROM
          CANDIDATE,
          CAND_SUMMARY,
          COMMITTEE,
          (
            SELECT state, sum(population) as state_pop from dist_pop
            GROUP BY 1
          )
  WHERE
          cand_pcc = cmte_id
          AND candidate.cand_id = cand_summary.cand_id
          AND CMTE_ST = state
  AND CAND_OFFICE = 'S'
  AND CAND_STATUS IN ('C', 'N')
  AND CAND_ELECTION_YR = 2016
  ORDER BY
          RECEIPTS_PER_CAPITA desc
  LIMIT 20;
