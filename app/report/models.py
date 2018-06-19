import datetime

from app.database import db, CRUDMixin


class Report(CRUDMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=False)
    rd_query = db.Column(db.Text(), nullable=True)
    created_ts = db.Column(
        db.DateTime(timezone=True),
        default=datetime.datetime.utcnow
    )
    updated_ts = db.Column(
        db.DateTime(timezone=True),
        default=datetime.datetime.utcnow
    )
    last_run = db.Column(
        db.DateTime(timezone=True),
        default=datetime.datetime.utcnow
    )

    def __init__(self, rd_query=None, **kwargs):
        super(Report, self).__init__(**kwargs)
        if rd_query:
            self.rd_query = rd_query

    def __repr__(self):
        return '<Report #%s:%r>' % (self.id, self.name)
