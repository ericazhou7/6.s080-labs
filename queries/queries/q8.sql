SELECT
        STATE,
        SUM(TRANSACTION_AMT)
    FROM
        INDIV_CONTRIB
    WHERE
        ENTITY_TP = "IND"
    GROUP BY
        1
    ORDER BY
        2 DESC;
