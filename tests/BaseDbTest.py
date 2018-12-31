from unittest import TestCase

from app import createApp, db
from tests.TestConfig import TestConfig


class BaseDbTest(TestCase):
    def setUp(self):
        app = createApp(TestConfig())
        app.app_context().push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()