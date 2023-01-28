select *
from users;

select user_id, count(*)
from daily_work
group by 1;

SELECT
                    case when
                        (select min(dw_date) from daily_work) < current_date
                    then 365
                    else current_date - (select min(dw_date) from daily_work) end
                from users limit 1;

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


SELECT case
           when
                   (select min(dw_date) from daily_work where user_id in (1)) < cast('2023-01-28' as date)
               then 365
           else
                   cast('2023-01-28' as date) - (select min(dw_date) from daily_work where user_id in (1))
           end as max_days_to_pull
from users
limit 1


SELECT
    cast('2023-01-28' as date) - (select min(dw_date) from daily_work where user_id in (1))
from users
limit 1