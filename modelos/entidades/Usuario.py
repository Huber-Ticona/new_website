from werkzeug.security import check_password_hash , generate_password_hash
from flask_login import UserMixin

class Usuario(UserMixin):

    def __init__(self,id ,usuario ,contrasena):
        self.id = id
        self.usuario = usuario
        self.contrasena = contrasena
        self.nombre = None
        self.apellido = None
        self.correo = None
        
    @classmethod
    def comprobar_contrasena(self,hash_contrasena,contrasena):
        if hash_contrasena == contrasena:
            return True
        else:
             return False
