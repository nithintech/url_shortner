from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class urlfield(Form):
    url = StringField('url',validators=[DataRequired()])
    out=StringField('out')
