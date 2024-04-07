from flask_login import UserMixin

from resiix.views.db import get_db

class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    @staticmethod
    def get(user_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM users.user WHERE id = %s", (user_id,)
        )
        user = cursor.fetchone()

        if not user:
            return None

        user = User(
            id_=user[0], name=user[1], email=user[2], profile_pic=user[3]
        )
        return user

    @staticmethod
    def create(id_, name, email, profile_pic):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO users.user (id, name, email, profile_pic) "
            "VALUES (%s, %s, %s, %s)",
            (id_, name, email, profile_pic),
        )
        db.commit()