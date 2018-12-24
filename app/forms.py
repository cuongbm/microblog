from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *

from app.models import User

class PostForm(FlaskForm):
    post = TextAreaField("Say something", validators=[DataRequired(), length(min=1, max=40)])
    submit = SubmitField("Submit")