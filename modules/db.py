from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Tool(db.Model):
    __tablename__ = "tools"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def __repr__(self):
        return '<Tool %r>' % self.name

class User(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def __repr__(self):
        return '<User %r>' % self.name
