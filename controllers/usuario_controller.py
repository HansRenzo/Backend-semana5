from flask_restful import Resource, request
from bcrypt import gensalt, hashpw
from dtos.usuario_dto import UsuarioDto
from db import conexion
from models.usuario_model import Usuario
from utils.enviar_correo import enviar_correo

class RegistroController(Resource):
    def post(self):
        data = request.json
        try:
            dto = UsuarioDto()
            data_serializada = dto.load(data)
            # Hash de la password
            salt = gensalt()
            password = bytes(data_serializada.get('password'),'utf-8')
            hashed_password = hashpw(password,salt).decode('utf-8')
            # ----- Fin hash de la password -----

            data_serializada['password'] = hashed_password
            nuevo_usuario = Usuario(**data_serializada)

            conexion.session.add(nuevo_usuario)
            

            enviar_correo(nuevo_usuario.correo, 'Bienvenido a libreria App', 
                          '''Bienvenido a esta nueva plataforma, donde encontrarás todo lo necesario para tus útiles de escritorio''')
            conexion.session.commit()
            return {
                'message': 'Usuario creado exitosamente'    
            }
        except Exception as error:
            conexion.session.rollback()
            return {
                'message': 'Error al registrar el usuario',
                'content': error.args
            }