SELECT
        CMTE_NM,
        SUM(TTL_RECEIPTS)
    FROM
        PAC_SUMMARY
    WHERE
        CMTE_TP = 'O'
    GROUP BY
        1
    ORDER BY
        2 DESC
    LIMIT 10;
