from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length
from email_validator import validate_email, EmailNotValidError

class Registrar_Cuenta_Form(FlaskForm):
    nombre = StringField('Nombre', validators=[InputRequired(),Length(min=3)])
    apellido = StringField('Apellido', validators=[InputRequired(),Length(min=3)])
    rut = StringField('RUT', validators=[InputRequired(),Length(max=10)])
    correo = StringField('Correo', validators=[InputRequired(), Email(),Length(min=8)])
    contraseña = PasswordField('Contraseña', validators=[InputRequired(), Length(min=8)])
    recaptcha = RecaptchaField()

    def validate_correo(form, field):
        try:
            validate_email(field.data)
        except EmailNotValidError as e:
            print(str(e))

class Login_Form(FlaskForm):
    correo = StringField('correo',validators=[InputRequired(), Email()])
    contraseña = StringField('Contraseña', validators=[InputRequired()])

class Correo_Form(FlaskForm):
    correo = StringField('Correo', validators=[InputRequired(), Email(),Length(min=8)])
    recaptcha = RecaptchaField()