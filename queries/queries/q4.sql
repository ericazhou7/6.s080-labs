SELECT cand_name, cmte_nm, cmte_st1 FROM CANDIDATE
JOIN COMMITTEE ON cand_pcc = cmte_id
          WHERE CAND_OFFICE = 'P'
          AND CAND_STATUS IN ('C', 'N')
          AND CAND_ELECTION_YR = 2016
          AND CAND_NAME like '%huck%';
