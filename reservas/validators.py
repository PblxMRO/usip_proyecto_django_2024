from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


validar_letras = RegexValidator(r'^[a-zA-Z\s]*$','Este campo solo puede contener letras')

def validar_correo_coorporativo(value):
    if "@medicdate.com" in value:
        return value
    else:
        raise ValidationError("El corrreo debe ser coorporativo (@medicdate.com)")

def validar_mayusculas(value):
    if not value.isupper():
        raise ValidationError("El texto debe estar en mayúsculas.")