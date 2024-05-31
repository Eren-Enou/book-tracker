from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, DateField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=200)])
    author = StringField('Author', validators=[Length(max=100)])
    genre = StringField('Genre', validators=[Length(max=50)])
    publication_date = DateField('Publication Date', format='%Y-%m-%d', validators=[DataRequired()])
    summary = TextAreaField('Summary', validators=[Length(max=1000)])
    rating = IntegerField('Rating', validators=[DataRequired()])
    status = SelectField('Status', choices=[('read', 'Read'), ('currently reading', 'Currently Reading'), ('want to read', 'Want to Read')], validators=[DataRequired()])
    date_started = DateField('Date Started', format='%Y-%m-%d', validators=[DataRequired()])
    date_finished = DateField('Date Finished', format='%Y-%m-%d')
    submit = SubmitField('Submit')