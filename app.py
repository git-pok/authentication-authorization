from flask import Flask, request, render_template, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import RegisterUserForm, LoginUserForm, FeedbackForm
from app_methods import flash_error, flash_success, delete_user_feedback_and_session
from app_methods import create_feedback, update_feedback, delete_feedback, create_db
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
# sqlalchemy database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///auth'
# sqlalchemy test database connection
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_tests'
# disable sqlalchemy track
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# enable sqlalchemy echo for terminal output when querying
app.config['SQLALCHEMY_ECHO'] = True
# flask secret key for debug toolbar
app.config['SECRET_KEY'] = 'blogly'
# this prevents the flask-debugtoolbar from intercepting route redirects
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# create flask-debugtoolbar app
debug = DebugToolbarExtension(app)
# connect the app to sqlalchemy
connect_db(app)
# debugger1
# import pdb
# pdb.set_trace()
# debugger2
# raise
with app.app_context():
    create_db(db)

@app.route('/')
def take_to_register_page():
    """
    redirects to /register
    """
    # db.drop_all()
    # db.create_all()
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    """returns register form"""
    # creates form
    form = RegisterUserForm()

    # checks for a post request and validates CSRF Token
    if form.validate_on_submit():
        # variables for method arguments
        # they are declared with wtf values
        username = form.username.data
        pwd = form.password.data
        eml = form.email.data
        fn = form.first_name.data 
        ln = form.last_name.data

        user = User.register(username, pwd, eml, fn, ln)
        db.session.add(user)
        # if these logics in try get put above the return,
        # they will run even if the code fails;
        # this led to unsuccessful registers gaining
        # access to the secret page.
        try:
            db.session.commit()
            session["username"] = user.username
            flash_success(f"Registered successfully {user.username}!") 
        except IntegrityError as exc:
            if exc.args[0].find('users_pkey') != -1:
                flash_error(f"Username {username} already exists!")
            else:
                flash_error(f"Email {eml} already exists!")
        return redirect('/secret')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    """logs user in"""
    # creates form
    form = LoginUserForm()
    if form.validate_on_submit():
        # variables for method arguments
        # they are declared with wtf values
        username = form.username.data
        pwd = form.password.data
        user = User.authenticate(username, pwd)
      
        if user:
            session["username"] = username
            flash_success(f"Welcome back {user.username}!")

            return redirect(f"/users/{username}")
        else:
            form.username.errors = ["Invalid credentials!"]
            return render_template('login.html', form=form)

    return render_template('login.html', form=form)

@app.route('/secret')
def secret_page():
    """
    checks session for logged in username
    responds with secret page if username exists
    """
    # if we dont use not in, or, gate = session.get("username", False),
    # we would get a KeyError if the session key is not found.
    if 'username' not in session:
        flash_error("Must be logged in to visit the secret page!")
        return redirect('/')
    else:
        return render_template('secret.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    logs user out
    clears session
    """
    if 'username' not in session:
        flash_error("Must be logged in to visit this page!")
        return redirect('/')
    else:
        session.clear()
        flash_success("Logged out successfully!")
        return redirect('/')

@app.route('/users/<username>')
def user_page(username):
    """
    responds with user details page
    """   
    user = User.query.filter_by(username=username).first()
    # we loop over this tuple in jinja template so we dont
    # have to make additional queries in jinja template
    try:
        feedback = db.session.query(
        Feedback.title,
        Feedback.content,
        Feedback.id
        ).join(User).filter(User.username == user.username).all()
    except AttributeError:
        flash_error(f"Username doesn't exist!")
        return redirect('/')
    # print('*********************************Running Query')
    # user_feedbacks = user.feedbacks[0]
    # print('*********************************Query Over')
    # print('*********************************Running Query')
    session_user = session.get('username', False)
    if username != session_user:
        flash_error("Must be logged in to visit that user page!")
        return redirect('/')
    else:
        return render_template('user.html', user=user,
        feedback=feedback, username=username)

@app.route('/users/<username>/delete', methods=['GET', 'POST'])
def delete_user(username):
    """
    deletes user instance from database
    """
    session_user = session.get("username", False)
    if 'username' not in session or session_user != username:
        flash_error("Can't visit this page!")
        return redirect('/')
    else:
        delete_user_feedback_and_session(username)
        flash_success("Deleted user successfully!")
        return redirect('/')

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback_form(username):
    """
    repsonds with feedback form
    """
    form = FeedbackForm()
    session_user = session.get('username', False)
    if username != session_user:
        flash_error("Cant visit that user feedback page!")
        return redirect('/')
    if form.validate_on_submit():
        # variables for method arguments
        # they are declared with wtf values
        titlef = form.title.data
        contentf = form.content.data
        usernamef = form.username.data
        create_feedback(titlef, contentf, usernamef)
        flash_success(f"Created feedback successfully {username}!")
        return redirect(f"/users/{username}")
    else:
        return render_template('feedback.html', form=form, username=username)

@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def feedback_edit_form(feedback_id):
    """
    repsonds with feedback edit form
    """
    feedback_query = Feedback.query.get_or_404(feedback_id)
    username = feedback_query.username
    form = FeedbackForm(obj=feedback_query)
    session_user = session.get('username', False)
    if username != session_user:
        flash_error("Cant visit that user feedback page!")
        return redirect(f"/users/{username}")
    if form.validate_on_submit():
        # variables for method arguments
        # they are declared with wtf values
        titlef = form.title.data
        contentf = form.content.data
        usernamef = form.username.data
        update_feedback(feedback_query, titlef, contentf, usernamef)
        flash_success(f"Edited feedback successfully {username}!")
        return redirect(f"/users/{username}")
    else:
        return render_template('feedback-edit.html', form=form)

@app.route('/feedback/<int:feedback_id>/delete', methods=['GET', 'POST'])
def feedback_delete(feedback_id):
    """
    deletes feedback from database
    """
    feedback_query = Feedback.query.get_or_404(feedback_id)
    username = feedback_query.username
    session_user = session.get('username', False)
    if username != session_user:
        flash_error("Cant visit that user feedback page!")
        return redirect(f"/users/{username}")
    else:
        delete_feedback(feedback_query)
        flash_success(f"Deleted feedback successfully {username}!")
        return redirect(f"/users/{username}")