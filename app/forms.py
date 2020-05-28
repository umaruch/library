from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired


class LoginRegisterForm(FlaskForm):
    name = StringField('Логин:', validators=[DataRequired()])
    password = PasswordField('Пароль:', validators=[DataRequired()])


class AuthorForm(FlaskForm):
    name = StringField('Имя автора:', validators=[DataRequired()])

class BookForm(FlaskForm):
    name = StringField('Название:', validators=[DataRequired()])
    date = StringField('Дата:', validators=[DataRequired()])
    author = SelectField('Автор:', coerce=int)
