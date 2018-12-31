from flask import request
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *

from app.models import User

class PostForm(FlaskForm):
    post = TextAreaField("Say something", validators=[DataRequired(), length(min=1, max=40)])
    submit = SubmitField("Submit")


class SearchForm(FlaskForm):
    q = StringField("Search", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if "formdata" not in kwargs:
            kwargs["formdata"] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False

        super(SearchForm, self).__init__(*args, **kwargs)

