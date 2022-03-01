import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    hash = db.Column(db.Integer)
    user_created_at = db.Column(db.DateTime)


class Sessions(db.Model):
    __tablename__ = 'sessions'
    sess_id = db.Column(db.Integer, primary_key=True)
    sess_datetime = db.Column(db.Date)
    number_sessions = db.Column(db.Integer)


class Calendar(db.Model):
    __tablename__ = 'calendar'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
