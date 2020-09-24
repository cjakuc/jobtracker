from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SubmitField, DateTimeField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User
from datetime import datetime

class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    password2 = PasswordField('Repeat Password',
                            validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # Methods that start with "validate_" are custom validators that
    ## WTForms will automatically invoke
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username is already in use, please select a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email is already in use, please select a different one')

class AddListingForm(FlaskForm):
    company = StringField('Company',
                          validators=[DataRequired(),
                          Length(min=0, max=140)])
    title = StringField('Title',
                        validators=[DataRequired(),
                        Length(min=0, max=140)])
    description = TextAreaField('Listing Text',
                                validators=[DataRequired()])
    location = StringField('Location',
                           validators=[DataRequired()])
    date_added = DateTimeField('Date Applied (yyyy-mm-dd)',
                               format='%Y-%m-%d',
                               default=datetime.utcnow())
    resume = StringField('Resume File Name',
                         validators=[DataRequired()])
    cover_letter = StringField('Cover Letter File Name',
                               validators=[DataRequired()])
    status = SelectField('Application Status',
                         choices=[('No Response'), ('Interviewing'), ('Rejected'), ('Received Offer'), ('Turned Down'), ('Accepted')],
                         coerce=str, validators=[DataRequired()],
                         default=('No Response'))
    submit = SubmitField('Add Listing')

class ViewEditListingForm(FlaskForm):
    company = StringField('Company',
                          validators=[DataRequired(),
                          Length(min=0, max=140)])
    title = StringField('Title',
                        validators=[DataRequired(),
                        Length(min=0, max=140)])
    description = TextAreaField('Listing Text',
                                validators=[DataRequired()])
    location = StringField('Location',
                           validators=[DataRequired()])
    date_added = DateTimeField('Date Applied (yyyy-mm-dd)',
                               format='%Y-%m-%d',
                               default=datetime.utcnow())
    resume = StringField('Resume File Name',
                         validators=[DataRequired()])
    cover_letter = StringField('Cover Letter File Name',
                               validators=[DataRequired()])
    status = SelectField('Application Status',
                         choices=[('No Response'), ('Interviewing'), ('Rejected'), ('Received Offer'), ('Turned Down'), ('Accepted')],
                         coerce=str, validators=[DataRequired()])
    submit = SubmitField('Update Listing')

class FilterListingsForm(FlaskForm):
    location = SelectField('Location', coerce=str, validators=[DataRequired()])
    status = SelectField('Application Status',
                         choices=[('No Response'), ('Interviewing'), ('Rejected'), ('Received Offer'), ('Turned Down'), ('Accepted'), ('Not rejected, turned down, or accepted'), ('All Statuses')],
                         coerce=str, validators=[DataRequired()],
                         default='All Statuses')
    submit = SubmitField('Filter')