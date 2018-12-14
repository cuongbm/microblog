import unittest
from app.models import *
from app import db


class ModelsTest(unittest.TestCase):
    def setUp(self):
        print("setup")
        users = User.query.all()
        for user in users:
            print(user)
            db.session.delete(user)
        db.session.commit()


    def test_createUser(self):
        print("test run")
        u = User(username="abc", email="testuser@email.com")
        db.session.add(u)
        db.session.commit()

