select cmte_nm, sum(TTL_RECEIPTS) from pac_summary
  where CMTE_TP = 'O'
  group by 1
  order by 2 desc
  limit 10;
