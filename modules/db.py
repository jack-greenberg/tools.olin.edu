from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

user_tool = db.Table('users_tools',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('tool_id', db.Integer, db.ForeignKey('tools.id'), primary_key=True),
    db.Column('level', db.Integer)
)

role_user = db.Table('role_user',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.role_id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

class Tool(db.Model):
    __tablename__ = "tools"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    shortname = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('tool-category.id'))
    category = db.relationship('ToolCategory')

    def __repr__(self):
        return '<Tool %r>' % self.name

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'))
    role = db.relationship('Role')
    tools_trained = db.relationship('Tool', secondary=user_tool, lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

class Role(db.Model):
    __tablename__ = "roles"
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(255))

    def __repr__(self):
        return self.role_name

class ToolCategory(db.Model):
    __tablename__ = "tool-category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
