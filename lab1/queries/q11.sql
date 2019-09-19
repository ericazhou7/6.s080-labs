-- Question: Of the 2016 Senate candidates, which had the n# of individual
-- contributions? List top 5 with cand_name and #. Use indiv_contrib and candidate tables.

SELECT
  CAND_NAME,
  COUNT(*) AS TOTAL_IND_CONTRIBS

FROM
  INDIV_CONTRIB,
  CANDIDATE

WHERE
  CAND_OFFICE = 'S'
  AND CAND_STATUS IN ('C', 'N')
  AND CAND_ELECTION_YR = 2016
  AND CAND_PCC = CMTE_ID
  AND ENTITY_TP = "IND"

GROUP BY
  CAND_NAME

ORDER BY
  TOTAL_IND_CONTRIBS DESC;
