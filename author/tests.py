import os
import unittest
import pathlib
from flask import session

from dotenv import load_dotenv
env_dir = pathlib.Path(__file__).parents[1]
load_dotenv(os.path.join(env_dir, '.flaskenv'))

from author.models import Author
from application import db
from application import create_app as create_app_base
from utils.test_db import TestDB


class AuthroTest(unittest.TestCase):
    def create_app(self):
        return create_app_base(
            SQLALCHEMY_DATABASE_URI=self.db_uri,
            TESTING=True,
            WTF_CSRF_ENABLED=False,
            SECRET_KEY='w\x04\x87\xb6\x03\xbaKf\xab\xba\xcf\xdec\x8a<\x117\xbf\xf7rj\xba\xc5^'
        )

    def setUp(self):
        self.test_db = TestDB()
        self.db_uri = self.test_db.create_db()
        self.app_factory = self.create_app()
        self.app = self.app_factory.test_client()
        with self.app_factory.app_context():
            db.create_all()


    def tearDown(self):
        with self.app_factory.app_context():
            db.drop_all()
        self.test_db.drop_db()


    def user_dict(self):
        return dict(
            full_name = 'aaaa aaa',
            email='a@aa.com',
            password='aaaa',
            confirm='aaaa'
        )



    def test_user_registration(self):
        rv = self.app.post('/register', data=self.user_dict(),
                           follow_redirects=True)
        assert 'You are now registered' in str(rv.data)

        with self.app as c:
            rv = c.get('/')
            assert Author.query.filter_by(email=self.user_dict()['email']).count() == 1


        rv = self.app.post('/register', data=self.user_dict(),
                           follow_redirects=True)
        assert 'Email already in use' in str(rv.data)

        user2 = self.user_dict()
        user2['email'] = 'bbb@bbb.com'
        user2['confirm'] = 'aaaaaaa'
        rv = self.app.post('/register', data=user2,
                           follow_redirects=True)
        assert 'Passwords must match' in str(rv.data)

    def test_user_log(self):
        rv = self.app.post('/register', data=self.user_dict())

        with self.app as c:
            rv = c.post('/login', data=self.user_dict(),
                        follow_redirects=True)

            assert session['id'] == 1

        with self.app as c:
            rv = c.get('/logout', follow_redirects=True)
            assert session.get('id') is None


        # bad pass
        user2 = self.user_dict()
        user2['password'] = 'test456'
        rv = self.app.post('/login', data=user2,
                           follow_redirects=True)
        assert 'Incorrect email or password' in str(rv.data)

        # bad email
        user3 = self.user_dict()
        user3['email'] = 'noo@blah.com'
        rv = self.app.post('/login', data=user3,
                           follow_redirects=True)
        assert 'Incorrect email or password' in str(rv.data)
