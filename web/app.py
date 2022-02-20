from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from static.helpers import login_required, pull_dataset

# Configure application
app = Flask(__name__)

# Add jinja zip option for multiple iterables
app.jinja_env.filters['zip'] = zip

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///deep.db")


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

    labels, datasets = pull_dataset(
        db=db,
        days_to_pull=14,
        rolling_sum_window=7,
        users=[session['user_id']]
        )
    print(datasets)
    return render_template("index.html", labels=labels, dataset=datasets[0])


@app.route("/social")
@login_required
def social():
    """Show social work summary"""
    labels, datasets = pull_dataset(db=db, days_to_pull=14, rolling_sum_window=7)

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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

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
        same_name = db.execute("SELECT id FROM users WHERE username = ?", user_name)

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

        db.execute("INSERT INTO users (username, hash, 	user_created_at)  VALUES (?, ?, CURRENT_TIMESTAMP)", username, hash)
        return redirect('/login')

    return render_template("register.html")


@app.route("/logout")
def logout():
    """Logout session"""

    # Forget any user_id
    session.clear()
    return redirect("/")

@app.route("/editSessions", methods=['POST'])
def editSessions():
    """Edit Session number"""
    user_id = session['user_id']
    date = request.form.get("date")
    sessions = request.form.get("sessions")
    if sessions.isnumeric() == False:
        flash("sessions must be a number greater than 0")
        return redirect('/')

    if int(sessions) < 0:
        flash("sessions must be a number greater than 0")
        return redirect('/')

    request.form.get("sessions")
    db.execute("DELETE FROM sessions where user_id = ? and sess_datetime = ?", user_id, date)
    db.execute("INSERT INTO sessions (user_id, sess_datetime, number_sessions)  VALUES (?, ?, ?)", user_id, date, sessions)

    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
