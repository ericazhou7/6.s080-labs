select cand_name, cand_office_st, SUM(TRANSACTION_AMT) from indiv_contrib a
join candidate b on a.cmte_id = b.cand_pcc 
where ENTITY_TP = "IND" AND CAND_OFFICE = 'S'
    AND CAND_STATUS IN ('C', 'N')
    AND CAND_ELECTION_YR = 2016
    AND a.state !=  b.cand_office_st
group by 1,2
order by 3 desc
limit 5;
