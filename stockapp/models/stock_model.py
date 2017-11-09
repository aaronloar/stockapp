
from stockapp import db


class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(12), index=True, unique=True)
    long_name = db.Column(db.String, index=True, unique=True)

    def __repr__(self):
        return "<Name {}>".format(self.name)


