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
    nombre = CharField(null=False)
    descripcion = TextField()
    expediente_numero = CharField()
    mano_obra = IntegerField()
    destacada = CharField(max_length=2)
    fecha_inicio = DateField()
    fecha_fin_inicial = DateField()
    plazo_meses = IntegerField()
    monto_contrato = FloatField()
    porcentaje_avance = IntegerField()
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
    comuna = IntegerField(null=False)
    def __str__(self):
        return self.barrio
    class Meta:
        db_table = 'Comunas'

class Etapa(BaseModel):
    id = AutoField(primary_key=True)
    etapa = CharField()
    def __str__(self):
        return self.etapa
    class Meta:
        db_table = 'Etapas'

class Empresa(BaseModel):
    id = AutoField(primary_key=True)
    licitacion_oferta_empresa = CharField()
    def __str__(self):
        return self.licitacion_oferta_empresa
    class Meta:
        db_table = 'Empresas'

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
    id_contratacion_tipo = ForeignKeyField(TipoContratacion, backref='contrataciones')
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
    id_obras = ForeignKeyField(Obra, backref='Relaciones')
    id_comuna = ForeignKeyField(Comuna, backref='Relaciones')
    id_area_responsable = ForeignKeyField(Area, backref='Relaciones')
    id_tipo = ForeignKeyField(TipoObra, backref='Relaciones')
    id_financiamiento = ForeignKeyField(FuenteFinanciamiento, backref='Relaciones')
    id_contratacion = ForeignKeyField(Contratacion, backref='Relaciones')
    id_etapas = ForeignKeyField(Etapa, backref='Relaciones')
    id_empresas = ForeignKeyField(Empresa, backref='Relaciones')
    def __str__(self):
        pass
    class Meta:
        db_table = 'Relaciones'