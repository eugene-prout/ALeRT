from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class EditGrammarForm(FlaskForm):
    grammar_editor = TextAreaField("Enter Your Grammar", validators=[DataRequired()])
    submit = SubmitField("Update Graph")
