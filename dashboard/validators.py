from datetime import datetime
from django.core.exceptions import ValidationError 

def validate_proposed_payment_date(value):
    if value <= datetime.today().date():
        raise ValidationError('Invalid date, Date must be greater than today')
    return value 