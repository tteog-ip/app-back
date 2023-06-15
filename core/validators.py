import re

from django.core.exceptions import ValidationError

def email_validate(email):
    REGEXR_EMAIL = '[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$'
    if not re.match(REGEXR_EMAIL, email):
        raise ValidationError('INVALID_KEY')

def password_validate(password):
    REGEXR_PASSWORD = '(?=.*[A-Za-z])(?=.*\d)(?=.*[~!@#$^&*()+|=])[A-Za-z\d~!@#$%^&*()+|=]{8,}'
    if not re.match(REGEXR_PASSWORD,password):
        raise ValidationError('INVALID_KEY')
