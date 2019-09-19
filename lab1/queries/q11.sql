-- Question: Of the 2016 Presidential candidates with the most donors, who received the highest contribution
-- per donor? List top 10 with cand_name and contribution per donor. Use indiv_contrib and candidate tables.

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
