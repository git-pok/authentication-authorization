from app import app
from models import db, connect_db, User, Feedback
from forms import RegisterUserForm, LoginUserForm, FeedbackForm
from app_methods import flash_error, flash_success, delete_user_feedback_and_session
from app_methods import create_feedback, update_feedback, delete_feedback, create_db 
from unittest import TestCase
from flask import session
from wtforms_test import FormTestCase
# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
# from sqlalchemy.exc import IntegrityError

# with app.app_context():
#     db.drop_all()
#     db.create_all()

app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class AuthenticationAppPythonMethods(TestCase):
    def setUp(self):
        """drop and create tables"""
        with app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        """drop tables"""
        with app.app_context():
            db.drop_all()

    # def test_create_db_row(self):
    #     """create_db_row returns the id of the created row; this tests that"""
    #     with app.app_context():
    #         self.assertEqual(User.register('BOWSER', '123456', 'b@icloud.com', 'Bowser', 'Powell'),
    #         <User username=BOWSER email=b@icloud.com first_name=Bowser last_name=Powell>)
    #         self.assertEqual(create_db_row('BOWSER', 'WARIO', 'www.test-bowser.com'), 2)

#     def test_create_db_row(self):
#         """create_db_row returns the id of the created row; this tests that"""
#         with app.app_context():
#             self.assertEqual(create_db_row('VINCENT', 'BRINXZ', 'www.test-vincent.com'), 1)
#             self.assertEqual(create_db_row('BOWSER', 'WARIO', 'www.test-bowser.com'), 2)

#     def test_delete_db_row(self):
#         """delete a row, verify its id, and verify 1 row is in table"""
#         with app.app_context():
#             create_db_row('VINCENT', 'BRINXZ', 'www.test-vincent.com')
#             create_db_row('BOWSER', 'WARIO', 'www.test-bowser.com')
#             delete_db_row(User.query.get(1))
#             self.assertEqual(len(User.query.all()), 1)
#             self.assertEqual(len(User.query.filter_by(id=2).all()), 1)

#     def test_delete_post_db_row(self):
#         """create_post_db_row returns the id of the created row; this tests that"""
#         with app.app_context():
#             create_db_row('Bowser', 'Wario', 'www.test-bowser.com')
#             create_db_row('Mario', 'Fwuuhh', 'www.test-mario.com')
#             create_post_db_row('TestTitle', 'TestContent', 1)
#             create_post_db_row('TestTitleII', 'TestContentII', 2)
#             post_id = Post.query.get_or_404(2)
#             delete_db_row(post_id)
#             self.assertEqual(len(Post.query.all()), 1)
#             self.assertEqual(len(Post.query.filter_by(id=1).all()), 1)

class AuthenticationAppFlaskIntegrationTests(TestCase):
    def setUp(self):
        """clean the query and create a User instance"""
        with app.app_context():
            User.query.delete()
            user = User.register('BOWSER', '123456', 'b@icloud.com', 'Bowser', 'Powell')
            # fb = Feedback('TitleTest', 'ContentTest', 'Bowser')
            db.session.add(user)
            # db.session.add(fb)
            db.session.commit()
            User.authenticate('BOWSER', '123456')
            # with app.test_client() as client:
            #     session["username"] = 'Bowser'
            # with app.test_client() as client:
            #     User.authenticate('BOWSER', '123456')

            # self.username = user.first_name
            # self.user = user

    def tearDown(self):
        """clean the session"""
        with app.app_context():
            db.session.rollback()
            # with app.test_client() as client:
            #     client.get('/logout')
                # session.clear()

    def test_home_redirect_to_register(self):
        """tests if / redirects to /register"""
        with app.app_context():
            with app.test_client() as client:
                resp = client.get('/')
                self.assertEqual(resp.status_code, 302)
                self.assertEqual(resp.location, '/register')

    def test_redirected_to_register_page(self):
        """tests the redirect from / to /register"""
        with app.app_context():
            with app.test_client() as client:
                resp = client.get('/', follow_redirects=True)
                html = resp.get_data(as_text=True)

                self.assertEqual(resp.status_code, 200)
                self.assertIn('<h1>Register Form</h1>', html)

#     def test_list_users(self):
#         """tests if /users lists users"""
#         with app.app_context():
#             with app.test_client() as client:
#                 resp = client.get('/users')
#                 html = resp.get_data(as_text=True)
#                 self.assertEqual(resp.status_code, 200)
#                 self.assertIn('Bowser', html)

    def test_login(self):
        """"""
        with app.app_context():
            with app.test_client() as client:
                # User.authenticate('BOWSER', '123456')
                login = {"username": 'Bowser', "password": '123456'}
                resp = client.post('/login', data=login, follow_redirects=True)
                # User.authenticate('BOWSER', '123456')
                # session["username"] = 'Bowser'
                # print(session["username"])
                html = resp.get_data(as_text=True)
                self.assertEqual(resp.status_code, 200)
                # self.assertEqual(session["username"], 'Bowser')
                # self.assertIn('<h1>Bowser</h1>', html)

    # def test_login_redirect(self):
    #     """tests if / redirects to /register"""
    #     with app.app_context():
    #         with app.test_client() as client:
    #             login = {"username": 'Bowser', "password": '123456'}
    #             resp = client.post('/login', data=login, follow_redirects=True)
    #             self.assertEqual(resp.status_code, 200)
    #             self.assertEqual(resp.location, '/users/Bowser')
    
    # def test_add_user(self):
    #     """"""
    #     with app.app_context():
    #         with app.test_client() as client:
    #             User.authenticate('BOWSER', '123456')
    #             fb = {"title": 'TitleTest', "content": 'ContentTest', "username": 'Bowser'}
    #             resp = client.post('/users/Bowser/feedback/add', data=fb, follow_redirects=True)
    #             html = resp.get_data(as_text=True)
    #             self.assertEqual(resp.status_code, 200)
    #             self.assertIn('<h1>Bowser</h1>', html)

    # def test_add_post(self):
    #     """tests if /user/submitted creates a user"""
    #     with app.app_context():
    #         with app.test_client() as client:
    #             add_post = {"post-title": 'TestTitle', "post-content": 'TestContent'}
    #             resp = client.post('/users/1/posts/new', data=add_post, follow_redirects=True)
    #             html = resp.get_data(as_text=True)
    #             self.assertEqual(resp.status_code, 200)
    #             self.assertIn('<li><a href="/posts/1">TestTitle</a></li>', html)