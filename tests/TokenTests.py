from app import db
from app.models import Token, User
from tests.BaseDbTest import BaseDbTest


class TokenTest(BaseDbTest):
    u1 = None

    def setUp(self):
        super(TokenTest, self).setUp()
        self.u1 = User(username='john', email='john@example.com')
        db.session.add(self.u1)


    def test_get_token_return_the_last_created(self):
        tk = Token.get_token(self.u1)
        db.session.commit()
        tk2 = Token.get_token(self.u1)
        self.assertEqual(tk.token, tk2.token)
        print(tk.user)


    def test_new_token_is_created_if_expired(self):
        tk = Token.get_token(self.u1)
        db.session.commit()
        tk.revoke()
        db.session.commit()
        tk2 = Token.get_token(self.u1)
        self.assertNotEqual(tk.token, tk2.token)
        db.session.commit()
        tk3 = Token.get_token(self.u1)
        self.assertEqual(tk2.token, tk3.token)

    def test_check_token(self):
        tk = Token.get_token(self.u1)
        db.session.commit()
        checked = Token.check(tk.token)
        self.assertIsNotNone(checked)
        checked.revoke()
        db.session.commit()
        self.assertIsNone(Token.check(tk.token))
