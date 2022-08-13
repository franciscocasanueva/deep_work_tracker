from flask import session, redirect
import functools


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


def rolling_sum(list_input, window):
    # TODO: Change this function to a recursion.
    rolling_list = []
    for i in range(len(list_input)):
        rolling_value = 0
        for w in range(window):
            if (i - w) > 0:
                rolling_value += list_input[i - w]
        rolling_list.append(rolling_value / float(window))
    return (rolling_list)


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
    days_to_pull_with_buffer = days_to_pull + rolling_sum_window

    result = conn.execute(
        """
            SELECT username, calendar.date as date, coalesce(sum(dw_minutes),0) as dw_minutes
            FROM calendar
            CROSS JOIN users
            left join daily_work as s on calendar.date = dw_date and users.id = s.user_id
            WHERE
                calendar.date > current_date - interval '{}' day
                and calendar.date <= current_date
                and users.id in {}
            GROUP BY user_created_at, username, calendar.date
            ORDER BY user_created_at asc, username, calendar.date ASC
        """.format(days_to_pull_with_buffer, users)
    )

    rows = [dict(row) for row in result.fetchall()]

    usernames = get_unique([x['username'] for x in rows])
    labels = get_unique([x['date'].strftime('%Y-%m-%d') for x in rows])[-days_to_pull:]

    datasets = []
    for username in usernames:
        dw_minutes = [x['dw_minutes'] for x in rows if x['username'] == username]
        x_day_average = rolling_sum(dw_minutes, rolling_sum_window)
        dataset = {
            'label': username,
            'dw_minutes': dw_minutes[-days_to_pull:],
            'x_day_average': x_day_average[-days_to_pull:]
        }
        datasets.append(dataset)

    return labels, datasets
