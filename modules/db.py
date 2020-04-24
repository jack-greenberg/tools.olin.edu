from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.attributes import QueryableAttribute

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True

    def to_dict(self, show=None, _hide=[], _path=None):
        """Return a dictionary representation of this model."""

        show = show or []

        hidden = self._hidden_fields if hasattr(self, "_hidden_fields") else []
        default = self._default_fields if hasattr(self, "_default_fields") else []
        default.extend(['id', 'modified_at', 'created_at'])

        if not _path:
            _path = self.__tablename__.lower()

            def prepend_path(item):
                item = item.lower()
                if item.split(".", 1)[0] == _path:
                    return item
                if len(item) == 0:
                    return item
                if item[0] != ".":
                    item = ".%s" % item
                item = "%s%s" % (_path, item)
                return item

            _hide[:] = [prepend_path(x) for x in _hide]
            show[:] = [prepend_path(x) for x in show]

        columns = self.__table__.columns.keys()
        relationships = self.__mapper__.relationships.keys()
        properties = dir(self)

        ret_data = {}

        for key in columns:
            if key.startswith("_"):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                ret_data[key] = getattr(self, key)

        for key in relationships:
            if key.startswith("_"):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                _hide.append(check)
                is_list = self.__mapper__.relationships[key].uselist
                if is_list:
                    items = getattr(self, key)
                    if self.__mapper__.relationships[key].query_class is not None:
                        if hasattr(items, "all"):
                            items = items.all()
                    ret_data[key] = []
                    for item in items:
                        ret_data[key].append(
                            item.to_dict(
                                show=list(show),
                                _hide=list(_hide),
                                _path=("%s.%s" % (_path, key.lower())),
                            )
                        )
                else:
                    if (
                        self.__mapper__.relationships[key].query_class is not None
                        or self.__mapper__.relationships[key].instrument_class
                        is not None
                    ):
                        item = getattr(self, key)
                        if item is not None:
                            ret_data[key] = item.to_dict(
                                show=list(show),
                                _hide=list(_hide),
                                _path=("%s.%s" % (_path, key.lower())),
                            )
                        else:
                            ret_data[key] = None
                    else:
                        ret_data[key] = getattr(self, key)

        for key in list(set(properties) - set(columns) - set(relationships)):
            if key.startswith("_"):
                continue
            if not hasattr(self.__class__, key):
                continue
            attr = getattr(self.__class__, key)
            if not (isinstance(attr, property) or isinstance(attr, QueryableAttribute)):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                val = getattr(self, key)
                if hasattr(val, "to_dict"):
                    ret_data[key] = val.to_dict(
                        show=list(show),
                        _hide=list(_hide),
                        _path=('%s.%s' % (path, key.lower())),
                    )
                else:
                    try:
                        ret_data[key] = json.loads(json.dumps(val))
                    except:
                        pass

        return ret_data

user_tool = db.Table('users_tools',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('tool_id', db.Integer, db.ForeignKey('tools.id'), primary_key=True),
    db.Column('level', db.Integer)
)

role_user = db.Table('role_user',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.role_id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

class Tool(BaseModel):
    __tablename__ = "tools"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    shortname = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('tool-category.id'))
    category = db.relationship('ToolCategory')

    _default_fields = ["name", "shortname", "category", "category_id"]

    def __repr__(self):
        return '<Tool %r>' % self.name

class User(BaseModel):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'))
    role = db.relationship('Role')
    tools_trained = db.relationship('Tool', secondary=user_tool, lazy='select')

    _default_fields = ['username', 'first_name', 'last_name', 'role', 'tools_trained']

    def __repr__(self):
        return '<User %r>' % self.username

class Role(BaseModel):
    __tablename__ = "roles"
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(255))

    def __repr__(self):
        return self.role_name

class ToolCategory(BaseModel):
    __tablename__ = "tool-category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    tools = db.relationship('Tool', backref='tool-category', lazy='joined')

    _default_fields = ["name"]

class Training(BaseModel):
    __tablename__ = "trainings"
    id = db.Column(db.Integer, primary_key=True)
    tool_id = db.Column(db.Integer, db.ForeignKey('tools.id'))
    tool = db.relationship('Tool')
    trainee_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    trainee = db.relationship('User')
    started = db.Column(db.DateTime)
    reading_complete = db.Column(db.Boolean)
    worksheet_complete = db.Column(db.Boolean)
    training_complete = db.Column(db.Boolean)
    testpiece_complete = db.Column(db.Boolean)
    #  logs = db.relationship("Log", backref="training", lazy=True)

#  class Log(db.Model):
    #  __tablename__ = "log"
    #  id = db.Column(db.Integer, primary_key=True)
    #  timestamp = db.Column(db.DateTime)
    #  training_id = db.Column(db.Integer, db.ForeignKey('training.id'))
    #  training = db.relationship("Training")
    #  text = db.Column(db.String(1023))
