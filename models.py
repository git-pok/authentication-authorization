from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
# creates sqlalchemy app
db = SQLAlchemy()
# initializes sqlalcehmey with our app
def connect_db(app):
    db.app = app
    db.init_app(app)

# instantiates bcrypt
bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'users'

    def __repr__(self):
	    usr = self
	    return f"<User username={usr.username} email={usr.email} first_name={usr.first_name} last_name={usr.last_name}>"

    username = db.Column(db.String(20), primary_key=True)

    password = db.Column(db.Text, nullable=False)

    email = db.Column(db.String(50), nullable=False, unique=True)

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)

    @classmethod
    def register(cls, username, pwd, eml, fn, ln):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8, email=eml, first_name=fn, last_name=ln)

    @classmethod
    def authenticate(cls, username, pwd):
        """
        Validate that user exists & password is correct.
        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False

class Feedback(db.Model):
    __tablename__ = 'feedback'

    def __repr__(self):
	    fb = self
	    return f"<Feedback title={fb.title} content={fb.content} username={fb.username}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(100), nullable=False)

    content = db.Column(db.Text, nullable=False)

    username = db.Column(db.String, db.ForeignKey('users.username'))