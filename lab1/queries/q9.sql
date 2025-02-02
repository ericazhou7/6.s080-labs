SELECT
  INDIV_CONTRIB.STATE,
  -- SUM(TRANSACTION_AMT),
  -- POPULATION,
  SUM(TRANSACTION_AMT)/POPULATION AS PER_CAPITA_CONTRIB
FROM
  INDIV_CONTRIB,
  (SELECT
      STATE,
      SUM(population) AS POPULATION
    FROM
        DIST_POP
    GROUP BY
        DIST_POP.STATE) AS DIST_POP

WHERE
  ENTITY_TP = "IND"
  AND TRANSACTION_TP = "10"
  AND DIST_POP.STATE = INDIV_CONTRIB.STATE

GROUP BY
  INDIV_CONTRIB.STATE

ORDER BY
  PER_CAPITA_CONTRIB DESC

LIMIT 5;
