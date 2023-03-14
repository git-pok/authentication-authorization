from flask_sqlalchemy import SQLAlchemy
from models import db, User, Feedback
from flask import flash, session
from forms import FeedbackForm

def flash_success(msg):
    """
    flashes message with success category
    """
    return flash(msg, "success")

def flash_error(msg):
    """
    flashes message with error category
    """
    return flash(msg, "error")

def create_db(db):
    """creates table and table object"""
    db.drop_all()
    db.create_all()
    # return User.query.all()

def delete_user_feedback_and_session(user):
    """
    deletes username from session
    deletes User from database
    """ 
    Feedback.query.filter_by(username=user).delete()
    User.query.filter_by(username=user).delete()
    db.session.commit()
    session.clear()

def create_feedback(titlef, contentf, usernamef):
    """creates Feedback instance and updates database"""
    feedback = Feedback(title=titlef, content=contentf, username=usernamef)
    db.session.add(feedback)
    db.session.commit()

def update_feedback(feedbackf, titlef, contentf, usernamef):
    """updates Feedback instance and updates database""" 
    feedbackf.title = titlef
    feedbackf.content = contentf
    feedbackf.username = usernamef
    db.session.add(feedbackf)
    db.session.commit()

def delete_feedback(feedbackf):
    """deletes Feedback instance and updates database""" 
    db.session.delete(feedbackf)
    db.session.commit()
