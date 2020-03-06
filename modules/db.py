from flask_sqlalchemy import SQLAlchemy

def init_db(app):
    return SQLAlchemy(app)

class Tool(object):
    pass

class User(object):
    pass
