from werkzeug.security import check_password_hash , generate_password_hash
from flask_login import UserMixin

class Usuario(UserMixin):

    def __init__(self,id , rut ,contrasena, nombre, apellido, correo):
        self.id = id
        self.rut = rut
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.contrasena = contrasena
        
    @classmethod
    def comprobar_contrasena(self,hash_contrasena,plain_contrasena):
        if check_password_hash(hash_contrasena, plain_contrasena):
            print('Las contraseñas coinciden')
            return True
        else:
             return False
