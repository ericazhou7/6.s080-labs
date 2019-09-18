select STATE, sum(TRANSACTION_AMT) from indiv_contrib
where ENTITY_TP = "IND"
group by 1;
