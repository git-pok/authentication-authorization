from app import app
from models import db, User, Feedback
# from flask_bcrypt import Bcrypt
# from flask_sqlalchemy import SQLAlchemy
from app_methods import create_db

with app.app_context():
    create_db(db)
    user = User.register('Bowser', '123456', 'b@icloud.com', 'Bowser', 'Powell')
    db.session.add(user)
    db.session.commit()