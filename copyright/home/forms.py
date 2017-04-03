from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, TextAreaField, validators

from copyright.models import db, User

class SignupForm(FlaskForm):
  firstname = StringField("First name", [
    validators.InputRequired()])
  lastname = StringField("Last name", [
    validators.InputRequired()])
  email = StringField("Email", [
    validators.InputRequired(),
    validators.Email("Please enter a valid email address.")])
  password = PasswordField('Password', [
    validators.InputRequired(),
    validators.Length(min=8, max=50, message="Password must be between 8 and 50 characters long.")])
  submit = SubmitField("Create account")
 
  def __init__(self, *args, **kwargs):
    FlaskForm.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not FlaskForm.validate(self):
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user:
      self.email.errors.append("An account with that email already exists.")
      return False
    else:
      return True

class LoginForm(FlaskForm):
  email = StringField("Email",[
    validators.InputRequired(),
    validators.Email("Please enter a valid email address.")])
  password = PasswordField('Password', [
    validators.InputRequired()])
  submit = SubmitField("Login")
   
  def __init__(self, *args, **kwargs):
    FlaskForm.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not FlaskForm.validate(self):
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user and user.check_password(self.password.data):
      return True
    else:
      self.email.errors.append("Invalid e-mail or password")
      return False


class ContactForm(FlaskForm):
  name = StringField("Name",[
    validators.InputRequired()])
  email = StringField("Email",[
    validators.InputRequired(),
    validators.Email("Please enter a valid email address.")])
  message = TextAreaField("Message", [
    validators.InputRequired()])
  submit = SubmitField("Submit")


class UpdateUserForm(FlaskForm):
  firstname = StringField("First name", [
    validators.InputRequired()])
  lastname = StringField("Last name", [
    validators.InputRequired()])
  password = PasswordField('Password', [
    validators.InputRequired(),
    validators.Length(min=8, max=50, message="Password must be between 8 and 50 characters long.")])
  plus_id = StringField("PLUS ID", [
    validators.Length(min=10, max=10, message="PLUS ID must be exactly 10 characters long.")]) ## TODO: should this be modifiable?
  submit = SubmitField("Update My Information")

  def validate(self):
    if not FlaskForm.validate(self):
      return False
     
    user = User.query.filter_by(plus_id = self.plus_id.data.lower()).first()
    if user:
      self.plus_id.errors.append("An account with that PLUS ID already exists.")
      return False
    else:
      return True