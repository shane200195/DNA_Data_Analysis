from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

class DNAEntry(FlaskForm):
    DNA = StringField('DNA', validators=[DataRequired()])
    Disease = StringField('Disease', validators=[DataRequired()])
    Description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Insert the data')

class DNADelete(FlaskForm):
    Disease = StringField('Disease', validators=[DataRequired()])
    submit = SubmitField('Delete the data')

class DNAUpdate(FlaskForm):
    DNA = StringField('Enter the new DNA')
    Disease = StringField('Enter the disease you want to update')
    Description = StringField('Enter the new description')
    submit = SubmitField('Update the data')

