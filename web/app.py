from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from static.helpers import login_required, pull_dataset
from db.db_tools import create_app
from db import config, db_tools, models

from sqlalchemy import create_engine, select
from sqlalchemy.sql import and_
from db.models import Users, Daily_work, Calendar

from datetime import datetime

# Configure application
app = create_app(__name__)

# Add jinja zip option for multiple iterables
app.jinja_env.filters['zip'] = zip

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

engine = create_engine(config.DATABASE_CONNECTION_URI)
conn = engine.connect()


# TODO: Test the impact of this response changes
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show work summary"""

    labels, datasets = pull_dataset(conn=conn, days_to_pull=14, rolling_sum_window=7, users=[session['user_id']])
    return render_template("index.html", labels=labels, dataset=datasets[0])


@app.route("/social")
@login_required
def social():
    """Show social work summary"""
    labels, datasets = pull_dataset(conn=conn, days_to_pull=14, rolling_sum_window=7)

    return render_template("social.html", labels=labels, datasets=datasets)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login page"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("must provide username")
            return redirect('/login')

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("must provide password")
            return redirect('/login')

        # Query database for username
        username = request.form.get("username")

        qry = select(Users).where(Users.username == username)
        result = conn.execute(qry)
        rows = [dict(row) for row in result.fetchall()]

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("invalid username and/or password")
            return redirect('/login')

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        return redirect("/")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Ensure username was submitted
    if request.method == 'POST':
        if not request.form.get("username"):
            flash("must provide username")
            return redirect('/register')

        user_name = request.form.get("username")
        qry = select(Users).where(Users.username == user_name)
        result = conn.execute(qry)
        same_name = [dict(row) for row in result.fetchall()]

        if len(same_name) != 0:
            flash("username taken")
            return redirect('/register')

        # Ensure password was submitted
        elif not request.form.get("password") or not request.form.get("confirmation"):
            flash("must provide password")
            return redirect('/register')

        # Ensure password and confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            flash("passwords must match")
            return redirect('/register')

        password = request.form.get("password")
        hash = generate_password_hash(password)
        username = request.form.get("username")

        db_tools.add_instance(
            Users,
            username=username,
            hash=hash,
            user_created_at=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        )

        return redirect('/login')

    return render_template("register.html")


@app.route("/logout")
def logout():
    """Logout session"""

    # Forget any user_id
    session.clear()
    return redirect("/")


@app.route("/editMinutes", methods=['POST'])
def editMinutes():
    """Edit Minutes number"""
    user_id = session['user_id']
    date = request.form.get("date")
    minutes = request.form.get("minutes")
    if not minutes.isnumeric():
        flash("Minutes must be a number greater than 0")
        return redirect('/')

    if int(minutes) < 0:
        flash("Minutes must be a number greater than 0")
        return redirect('/')

    request.form.get("minutes")

    # Delete old entry for that day
    qry = select(Daily_work.id).where(and_(user_id == user_id, Daily_work.dw_date == date))
    result = conn.execute(qry)
    rows = [dict(row) for row in result.fetchall()]

    if len(rows) == 1:
        id_to_delete = rows[0]['id']
        db_tools.delete_instance(
            Daily_work,
            id_to_delete
        )

    # Add new entry for that date
    db_tools.add_instance(
        Daily_work,
        user_id=user_id,
        dw_date=date,
        dw_minutes=minutes
    )

    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
