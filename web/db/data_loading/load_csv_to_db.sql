select *
from users;

select user_id, count(*)
from daily_work
group by 1;

select * from daily_work

select *
from calendar
where calendar.date <= current_date
order by 1 desc; --desc


SELECT username, calendar.date as date, coalesce(sum(dw_minutes), 0) as dw_minutes
FROM calendar
         CROSS JOIN (select id, username, user_created_at from users where id in (1)) as users
         left join daily_work as s on calendar.date = dw_date and users.id = s.user_id
WHERE calendar.date > current_date - interval '5' day
  and calendar.date <= current_date
GROUP BY user_created_at, username, calendar.date
ORDER BY user_created_at asc, username, calendar.date ASC;


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