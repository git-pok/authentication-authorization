from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length

class RegisterUserForm(FlaskForm):
    """
    form for registering user
    """

    username = StringField('Username', validators=[
    InputRequired(message='Username can"t be blank!'),
    Length(min=0, max=20, message='Username must be atleast 0 characters long but no longer than 20!')
    ])

    password = PasswordField('Password', validators=[
    InputRequired(message='Password must be filled!')
    ])

    email = StringField('Email', validators=[
    InputRequired(message='Email must be filled!'),
    Length(min=0, max=50, message='email must be atleast 0 characters long but no longer than 50!')
    ])

    first_name = StringField('First Name', validators=[
    InputRequired(message='First name must be filled!'),
    Length(min=0, max=30, message='First Name must be atleast 0 characters long but no longer than 30!')
    ])

    last_name = StringField('Last Name', validators=[
    InputRequired(message='Last name must be filled!'),
    Length(min=0, max=30, message='Last name must be atleast 0 characters long but no longer than 30!')
    ])

class LoginUserForm(FlaskForm):
    """
    form to login user
    """

    username = StringField('Username', validators=[
    InputRequired(message='Username can"t be blank!'),
    Length(min=0, max=20, message='Username must be atleast 0 characters long but no longer than 20!')
    ])

    password = PasswordField('Password', validators=[
    InputRequired(message='Password must be filled!')
    ])

class FeedbackForm(FlaskForm):
    """
    form to add feedback
    """

    title = StringField('Title', validators=[
    InputRequired(message='Title name must be filled!'),
    Length(min=0, max=100, message='Title name must be atleast 0 characters long but no longer than 100!')
    ])

    content = StringField('Content',
    validators=[InputRequired(message='Content name must be filled!')]
    )

    username = StringField('Username',
    validators=[InputRequired(message='Username name must be filled!')]
    )