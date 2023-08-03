from flask import request
from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length

class EditGrammarForm(FlaskForm):
    grammar_editor = TextAreaField('Enter Your Grammar', validators=[DataRequired()])
