select *
from users;

select user_id, count(*)
from daily_work
group by 1;

select *
from calendar
order by 2 asc --desc


select
    getid(),
    1 as user_id,
    day as dw_date,
    paco as dw_minutes
from bv_raw_data;

select * from bv_raw_data

SELECT
    4,
    cast(day as date),
    cast(tabixe as int)
--     cast(case
--         when coalesce(cutice, '') = '' then '0'
--         else cutice
--     end as int)
FROM bv_raw_data

delete from daily_work;