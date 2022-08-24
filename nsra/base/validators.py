from django.core.validators import RegexValidator
from nsra.constants import PHONE

phone_validator = RegexValidator(regex=PHONE, message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")