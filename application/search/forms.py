
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired


class BookForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    shelf = StringField('shelf', validators=[DataRequired()])
    block = TextAreaField('block', validators=[DataRequired()])
    writer = StringField('writer', validators=[DataRequired()])
    loan = SelectField('loan', choices=[("False", "False"), ("True", "True")], validators=[DataRequired()])
    submit = SubmitField("Add todo")
