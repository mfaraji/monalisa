from flask_wtf import Form

from wtforms import DateField, SelectMultipleField
from wtforms.validators import DataRequired

from sqlalchemy import create_engine

en = create_engine('redshift+psycopg2://rs_adhoc_usr:R5adL0cK@insp-dw-prod01.cogvbioiyusk.us-west-2.redshift.amazonaws.com:5439/bdm')

query = """
Select lower(Contract) as Contract
from bdm.Affiliate
Where ContractStatus = 'Active'
group by Contract order by lower(Contract)
"""

result = en.execute(query)

CHOICES = [(value[0], value[0]) for index, value in enumerate(result)]

class ReportForm(Form):
    from_date = DateField('From Date', format='%m/%d/%Y', validators=[DataRequired()])
    to_date = DateField('To Date', format='%m/%d/%Y', validators=[DataRequired()])
    contracts = SelectMultipleField(
        'Contracts', choices=CHOICES, validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
