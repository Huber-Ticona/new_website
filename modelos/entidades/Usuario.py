from werkzeug.security import check_password_hash , generate_password_hash

class Usuario():

    def __init__(self,usuario ,contrasena):
        self.usuario_id = None
        self.usuario = usuario
        self.contrasena = contrasena
        self.nombre = None
        self.apellido = None
        self.correo = None
    
    def comprobar_contrasena(self,hash_contrasena,contrasena):
        pass
