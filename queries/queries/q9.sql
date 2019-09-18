select a.STATE, sum(TRANSACTION_AMT)/population as AMT_PER_CAPITA from indiv_contrib a
where ENTITY_TP = "IND" and TRANSACTION_TP = "10"
join dist_pop b on a.STATE = b.state 
group by 1
order by 2 desc
limit 5;
