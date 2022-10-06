select *
from users;

select *
from daily_work;

select *
from calendar
order by 2 asc --desc


select
    getid(),
    1 as user_id,
    day as dw_date,
    paco as dw_minutes
from bv_raw_data;


INSERT INTO daily_work ( user_id, dw_date, dw_minutes)
SELECT
    4,
    cast(day as date),
    cast(case
        when coalesce(kim, '') = '' then '0'
        else kim
    end as int)
FROM bv_raw_data;


INSERT INTO daily_work ( user_id, dw_date, dw_minutes)
SELECT
    5,
    cast(day as date),
    cast(tabixe as int)
--     cast(case
--         when coalesce(cutice, '') = '' then '0'
--         else cutice
--     end as int)
FROM bv_raw_data;


SELECT
    4,
    cast(day as date),
    cast(tabixe as int)
--     cast(case
--         when coalesce(cutice, '') = '' then '0'
--         else cutice
--     end as int)
FROM bv_raw_data