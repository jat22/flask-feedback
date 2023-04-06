from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import InputRequired, Length

class RegistrationForm(FlaskForm):
	"""registration form"""

	username = StringField("Username", validators=[InputRequired(), Length(max=20)])

	password = PasswordField("Password", validators=[InputRequired()])
	
	email = EmailField("Email", validators=[InputRequired(), Length(max=50)])
	
	first_name = StringField("First Name", validators=[InputRequired(), Length(max=30)])
	
	last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30)])


class LoginForm(FlaskForm):
	"""login form"""

	username = StringField("Username", validators=[InputRequired()])

	password = PasswordField("Password", validators=[InputRequired()])

class FeedbackForm(FlaskForm):
	"""add feedback"""

	title = StringField("Title", validators=[InputRequired()])

	content = TextAreaField("Comments", validators=[InputRequired()])
