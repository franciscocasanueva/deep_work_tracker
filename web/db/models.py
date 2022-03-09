import flask_sqlalchemy

from sqlalchemy import event

db = flask_sqlalchemy.SQLAlchemy()


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    hash = db.Column(db.String(500))
    user_created_at = db.Column(db.DateTime)


class Sessions(db.Model):
    __tablename__ = 'sessions'
    sess_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    sess_datetime = db.Column(db.Date)
    number_sessions = db.Column(db.Integer)


class Calendar(db.Model):
    __tablename__ = 'calendar'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)


def insert_calendar(target, connection, **kw):
    """
    Make sure the calendar table is created the first time the model is run
    """
    connection.execute(
        """
        insert into calendar (id, date)
        SELECT
            ROW_NUMBER() over() as id,
            CAST('2015-01-01' AS DATE) + (n || ' day')::INTERVAL as date
        FROM    generate_series(0, 10000) n
        """
    )


event.listen(Calendar.__table__, 'after_create', insert_calendar)
