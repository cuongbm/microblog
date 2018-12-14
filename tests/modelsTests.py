import unittest
from app.models import *

class ModelsTest(unittest.TestCase):
    def test_createUser(self):
        u = User(username="abc")
        self.assertEqual(u.__repr__(), "<User abc>")
        print(u)
