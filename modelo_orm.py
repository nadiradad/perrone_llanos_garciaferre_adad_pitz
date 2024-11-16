"""Crear el módulo “modelo_orm.py” que contenga la definición de las clases y atributos que
considere necesarios, siguiendo el modelo ORM de Peewee para poder persistir los datos
importados del dataset en una base de datos relacional de tipo SQLite llamada
“obras_urbanas.db”, ubicada en la misma carpeta solución del proyecto. Aquí se debe incluir
además la clase BaseModel heredando de peewee.Model."""

from peewee import *

sqlite_db = SqliteDatabase('/obras_urbanas.db', pragmas={'journal_mode': 'wal'})

try:
    sqlite_db.connect()
except OperationalError as e:
    print("Error al conectar con la BD.", e)
    exit()

class BaseModel(Model):
    class Meta:
        database = sqlite_db