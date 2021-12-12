from flask_login import UserMixin
from model.mysql import conn_mysql


class User(UserMixin):
    def __init__(self, user_id, user_email, blog_id):
        self.id = user_id
        self.user_email = user_email
        self.blog_id = blog_id

    def get_id(self):
        return str(self.id)
