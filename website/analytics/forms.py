from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length

class ClassificationForm(FlaskForm):
    picture = FileField('Submit a pet image for classification!', validators=[FileAllowed(['jpg', 'png', 'tif', 'gif', 'mov'])])
    submit = SubmitField('Analyze Image')