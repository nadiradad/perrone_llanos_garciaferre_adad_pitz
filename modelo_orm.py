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

class Obra(BaseModel):
    id = AutoField(primary_key=True)
    nombre = CharField()
    descripcion = TextField()
    expediente_numero = CharField()
    mano_obra = IntegerField()
    destacada = CharField(max_length=2)
    fecha_inicio = DateField()
    fecha_fin_inicial = DateField()
    plazo_meses = IntegerField()
    def __str__(self):
        return self.nombre
    class Meta:
        db_table = 'Obras'

class Area(BaseModel):
    id = AutoField(primary_key=True)
    area_responsable = CharField()
    def __str__(self):
        return self.area_responsable
    class Meta:
        db_table = 'Areas'

class FuenteFinanciamiento(BaseModel):
    id = AutoField(primary_key=True)
    financiamiento = CharField()
    def __str__(self):
        return self.financiamiento
    class Meta:
        db_table = 'FuenteFinanciamientos'

class Comuna(BaseModel):
    id = AutoField(primary_key=True)
    barrio = CharField()
    comuna = IntegerField()
    def __str__(self):
        return self.barrio
    class Meta:
        db_table = 'Comunas'

class Etapa(BaseModel):
    id = AutoField(primary_key=True)
    etapa = CharField()
    porcentaje_avance = IntegerField()
    def __str__(self):
        return self.etapa
    class Meta:
        db_table = 'Etapas'

class Licitacion(BaseModel):
    id = AutoField(primary_key=True)
    licitacion_oferta_empresa = CharField()
    monto_contrato = FloatField()
    def __str__(self):
        return self.licitacion_oferta_empresa
    class Meta:
        db_table = 'Licitaciones'

class TipoContratacion(BaseModel):
    id = AutoField(primary_key=True)
    contratacion_tipo = CharField()
    def __str__(self):
        return self.contratacion_tipo
    class Meta:
        db_table = 'TipoContrataciones'

class Contratacion(BaseModel):
    id = AutoField(primary_key=True)
    nro_contratacion = CharField()
    id_contratacion_tipo = ForeignKeyField(TipoContratacion, backref='id')
    def __str__(self):
        return self.nro_contratacion
    class Meta:
        db_table = 'Contrataciones'


class TipoObra(BaseModel):
    id = AutoField(primary_key=True)
    tipo = CharField()
    def __str__(self):
        return self.tipo
    class Meta:
        db_table = 'TipoObras'

class Relacion(BaseModel):
    id = AutoField(primary_key=True)
    id_obras = ForeignKeyField(Obra, backref='id')
    id_comuna = ForeignKeyField(Comuna, backref='id')
    id_area_responsable = ForeignKeyField(Area, backref='id')
    id_tipo = ForeignKeyField(TipoObra, backref='id')
    id_financiamiento = ForeignKeyField(FuenteFinanciamiento, backref='id')
    id_contratacion = ForeignKeyField(Contratacion, backref='id')
    id_etapas = ForeignKeyField(Etapa, backref='id')
    id_licitaciones = ForeignKeyField(Licitacion, backref='id')
    def __str__(self):
        pass
    class Meta:
        db_table = 'Relaciones'