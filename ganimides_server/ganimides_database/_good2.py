from sqlalchemy.sql.expression import not_

class BaseModel(db.Model):
    __abstract__ = True

    def __init__(self, **kwargs):
        kwargs["_force"] = True
        self.from_dict(**kwargs)

    def to_dict(self, show=None, _hide=[], _path=None):
        ...

    def from_dict(self, **kwargs):
        """Update this model with a dictionary."""

        _force = kwargs.pop("_force", False)

        readonly = self._readonly_fields if hasattr(self, "_readonly_fields") else []
        if hasattr(self, "_hidden_fields"):
            readonly += self._hidden_fields

        readonly += ["id", "created_at", "modified_at"]

        columns = self.__table__.columns.keys()
        relationships = self.__mapper__.relationships.keys()
        properties = dir(self)

        changes = {}

        for key in columns:
            if key.startswith("_"):
                continue
            allowed = True if _force or key not in readonly else False
            exists = True if key in kwargs else False
            if allowed and exists:
                val = getattr(self, key)
                if val != kwargs[key]:
                    changes[key] = {"old": val, "new": kwargs[key]}
                    setattr(self, key, kwargs[key])

        for rel in relationships:
            if key.startswith("_"):
                continue
            allowed = True if _force or rel not in readonly else False
            exists = True if rel in kwargs else False
            if allowed and exists:
                is_list = self.__mapper__.relationships[rel].uselist
                if is_list:
                    valid_ids = []
                    query = getattr(self, rel)
                    cls = self.__mapper__.relationships[rel].argument()
                    for item in kwargs[rel]:
                        if (
                            "id" in item
                            and query.filter_by(id=item["id"]).limit(1).count() == 1
                        ):
                            obj = cls.query.filter_by(id=item["id"]).first()
                            col_changes = obj.from_dict(**item)
                            if col_changes:
                                col_changes["id"] = str(item["id"])
                                if rel in changes:
                                    changes[rel].append(col_changes)
                                else:
                                    changes.update({rel: [col_changes]})
                            valid_ids.append(str(item["id"]))
                        else:
                            col = cls()
                            col_changes = col.from_dict(**item)
                            query.append(col)
                            db.session.flush()
                            if col_changes:
                                col_changes["id"] = str(col.id)
                                if rel in changes:
                                    changes[rel].append(col_changes)
                                else:
                                    changes.update({rel: [col_changes]})
                            valid_ids.append(str(col.id))

                    # delete rows from relationship that were not in kwargs[rel]
                    for item in query.filter(not_(cls.id.in_(valid_ids))).all():
                        col_changes = {"id": str(item.id), "deleted": True}
                        if rel in changes:
                            changes[rel].append(col_changes)
                        else:
                            changes.update({rel: [col_changes]})
                        db.session.delete(item)

                else:
                    val = getattr(self, rel)
                    if self.__mapper__.relationships[rel].query_class is not None:
                        if val is not None:
                            col_changes = val.from_dict(**kwargs[rel])
                            if col_changes:
                                changes.update({rel: col_changes})
                    else:
                        if val != kwargs[rel]:
                            setattr(self, rel, kwargs[rel])
                            changes[rel] = {"old": val, "new": kwargs[rel]}

        for key in list(set(properties) - set(columns) - set(relationships)):
            if key.startswith("_"):
                continue
            allowed = True if _force or key not in readonly else False
            exists = True if key in kwargs else False
            if allowed and exists and getattr(self.__class__, key).fset is not None:
                val = getattr(self, key)
                if hasattr(val, "to_dict"):
                    val = val.to_dict()
                changes[key] = {"old": val, "new": kwargs[key]}
                setattr(self, key, kwargs[key])

        return changes

Using the new from_dict method we update our user with a dictionary:

updates = {
    "username": "zoe",
    "email_confirmed": True,
}
user.from_dict(**updates)
db.session.commit()
from_dict

print(user.to_dict(show=['email_confirmed']))
Which prints:

{
    'id': UUID('488345de-88a1-4c87-9304-46a1a31c9414'),
    'username': 'zoe',
    'email_confirmed': None,
    'joined_recently': True,
    'modified_at': datetime.datetime(2018, 7, 11, 6, 36, 47, 939084),
    'created_at': datetime.datetime(2018, 7, 11, 6, 28, 56, 905379),
}
Notice that email_confirmed is still None because it’s marked as read only.

Relationships
Our to_dict and from_dict methods also work for relationships. For example, when our User model has many Goal models we can serialize Goal by default or with show:

class User(BaseModel):
    ...
    goals = db.relationship('Goal', backref='user', lazy='dynamic')

class Goal(BaseModel):
    id = db.Column(UUID(), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(), nullabe=False)
    accomplished = db.Column(db.Boolean())
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

    _default_fields = [
        "title",
    ]

goal = Goal(title="Mountain", accomplished=True)
user.goals.append(goal)
db.session.commit()

print(user.to_dict(show=['goals', 'goals.accomplished']))
Which prints:

{
    'id': UUID('488345de-88a1-4c87-9304-46a1a31c9414'),
    'username': 'zoe',
    'goals': [
        {
            'id': UUID('c72cfef0-0988-45e4-9f4b-8a4a7d4f8d8f'),
            'title': 'Mountain',
            'accomplished': True,
            'created_at': datetime.datetime(2018, 7, 11, 6, 45, 18, 299924),
        },
    ],
    'joined_recently': True,
    'modified_at': datetime.datetime(2018, 7, 11, 6, 36, 47, 939084),
    'created_at': datetime.datetime(2018, 7, 11, 6, 28, 56, 905379),
}
It even allows customizing columns of relationships, for ex: goals.accomplished.

To see how this all fits into a RESTful API continue with Part 2: Building a Flask RESTful API.