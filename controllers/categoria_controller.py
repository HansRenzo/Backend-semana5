from flask_restful import Resource, request
from flask import send_file
from werkzeug.utils import secure_filename
from os import path
# universal unique identifier
from uuid import uuid4
from dtos.categoria_dto import CategoriaDto
from db import conexion
from models.categoria_model import Categoria
from sqlalchemy.orm import Query

class ImagenesController(Resource):
    def post(self):
        # Si nosotros queremos enviar informacion por el form-data ahora utilizaremos la propiedad 'form'
        print(request.form)
        # Para obtener las llaves que contengan archivos 'files'
        print(request.files)
        
        imagen = request.files.get('imagen')

        print(imagen.filename)
        # save sirve para guardar la imagen, pero utilizamos el secure_filename para que sea un nombre valido
        nombre_seguro = secure_filename(uuid4().hex + '-' + imagen.filename)

        imagen.save(path.join('imagenes', nombre_seguro))

        return {
            'message': 'Categoria creada exitosamente'
        }

    def get(self, nombre):
        try:
            return send_file(path.join('imagenes',nombre))
        except FileNotFoundError:
            return send_file(path.join('imagenes','not_found.png'))
        
class CategoriasController(Resource):
    def post(self):
        mimetype_valido = 'image/'
        data = request.form.to_dict()
        try:
            imagen = request.files.get('imagen')
            print(imagen.filename)
            if mimetype_valido not in imagen.mimetype:
                raise Exception('El archivo no es un archivo válido')
            
            dto = CategoriaDto()
            nombre = secure_filename(uuid4().hex + '-' + imagen.filename)

            data['imagen'] = 'imagenes/' + nombre
            data_serializada =dto.load(data)

            nueva_categoria = Categoria(**data_serializada)
            conexion.session.add(nueva_categoria)

            imagen.save(path.join('imagenes', nombre))

            conexion.session.commit()
            
            #print(imagen.mimetype)
            return {
                'message': 'Categoria creada correctamente'
            }
        except Exception as error:
            conexion.session.rollback()
            return {
                'message': 'Error al crear la categoría',
                'content': error.args
            }
    def get(self):
        query = conexion.session.query(Categoria)
        resultado = query.all()
        dto = CategoriaDto()
        data = dto.dump(resultado, many=True)

        return {
            'content': data
        }

