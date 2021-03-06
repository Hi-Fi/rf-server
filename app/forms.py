from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class ArgumentForm(FlaskForm):
    argument1 = StringField('argument1', validators=[DataRequired()], default='argument1')
    argument2 = StringField('argument2', validators=[DataRequired()], default='argument2')
    secret_argument = PasswordField('secret_argument', validators=[DataRequired()], default='secret_argument')
    test_suite = SelectField('test_suite', validators=[DataRequired()])
    submit = SubmitField('Start run')

