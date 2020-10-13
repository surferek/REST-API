from ..code.database import db


class UserModel(db.Model):
    """
    This is API that expose two methods to other programs:
    find_by_username and find_by_id
    """
    __tablename__ = 'users'

    # These properties must match whats in __init__
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    password = db.Column(db.String(32))

    def __init__(self, username, password):
        self.username = username
        self.password = password

        # Property below will belong to the object but not used by database
        self.some_variable = "This is some non-database variable"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()


    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()


