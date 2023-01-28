from flask import session, redirect
import functools
import time
from datetime import date

def login_required(f):
    """
    Decorate routes to require login.
    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """

    @functools.wraps(f)
    def decorated_fuction(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_fuction

def get_unique(seq):
    """
    Create an order list of unique values from a list
    """
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def pull_dataset(conn, days_to_pull, rolling_sum_window, users=None):
    """
    From a list of users pull working minutes dataset
    """
    if not users:
        result = conn.execute(
            """
            SELECT distinct(id) as user_id
            FROM users;
        """)
        users = [dict(row) for row in result.fetchall()]
        users = [x['user_id'] for x in users]

    # Format inputs for query
    users = [str(x) for x in users]
    users = "('" + "', '".join(users) + "')"

    today_ts = time.strftime('%Y-%m-%d')
    if days_to_pull == 'max':
        get_max_days_to_pull = f"""
            SELECT
                cast('2023-01-28' as date) - (select min(dw_date) from daily_work where user_id in (1)) as max_days_to_pull
            from users
            limit 1"""
        result = conn.execute(get_max_days_to_pull)
        rows = [dict(row) for row in result.fetchall()]
        days_to_pull = int(rows[0]['max_days_to_pull'])

    days_to_pull_with_buffer = days_to_pull + rolling_sum_window
    days_to_pull_with_buffer = max(days_to_pull_with_buffer, 365+90)
    get_history_qry = f"""
    SELECT 
            username, 
            calendar.date as date, 
            coalesce(sum(dw_minutes), 0) as dw_minutes
        FROM calendar
                 CROSS JOIN (select id, username, user_created_at from users where id in {users}) as users
                 left join daily_work as s on calendar.date = dw_date and users.id = s.user_id
        WHERE calendar.date > cast('{today_ts}' as date) - interval '{days_to_pull_with_buffer}' day
          and calendar.date <= cast('{today_ts}' as date) 
        GROUP BY user_created_at, username, calendar.date
        ORDER BY user_created_at asc, username, calendar.date ASC"""

    result = conn.execute(get_history_qry)
    rows = [dict(row) for row in result.fetchall()]

    usernames = get_unique([x['username'] for x in rows])
    # Labels is not needed It is not used
    x_labels = get_unique([x['date'].strftime('%Y-%m-%d') for x in rows])[-days_to_pull_with_buffer:]

    datasets = []
    for username in usernames:
        dw_minutes = [x['dw_minutes'] for x in rows if x['username'] == username]
        x_day_average = dw_minutes
        dataset = {
            'label': username,
            'dw_minutes': dw_minutes[-days_to_pull_with_buffer:],
            'x_day_average': x_day_average[-days_to_pull_with_buffer:],
            'x_labels': x_labels
        }
        datasets.append(dataset)

    return datasets
