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
    comuna = IntegerField(null=False)
    def __str__(self):
        return self.comuna
    class Meta:
        db_table = 'Comunas'

class Barrio(BaseModel):
    id = AutoField(primary_key=True)
    barrio = CharField()
    id_comuna = IntegerField(null=False)
    def __str__(self):
        return self.barrio
    class Meta:
        db_table = 'Barrios'

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
    id_barrio = ForeignKeyField(Barrio, backref='Obras')
    id_area_responsable = ForeignKeyField(Area, backref='Obras')
    id_tipo = ForeignKeyField(TipoObra, backref='Obras')
    id_financiamiento = ForeignKeyField(FuenteFinanciamiento, backref='Obras')
    id_contratacion = ForeignKeyField(Contratacion, backref='Obras')
    id_etapas = ForeignKeyField(Etapa, backref='Obras')
    id_empresas = ForeignKeyField(Empresa, backref='Obras')
    def __str__(self):
        return self.nombre
    class Meta:
        db_table = 'Obras'
    def nuevo_proyecto(self)->bool:
       try:
           etapa_encontrada, created= Etapa.get_or_create(Etapa.etapa == 'Proyecto')
           if created == True:
               print(f"La etapa proyecto no existía y se ha creado en la bbdd")
           else:
                print(f"Etapa del proyecto encontrada")
           self.id_etapas = etapa_encontrada.id
           return True
       except Exception as e:
           print(f"Error: {e}")
           return False

    def iniciar_contratacion(nro_contratacion, contratacion_tipo):
        try:
            tipo_contratacion_encontrada = TipoContratacion.get_or_none(TipoContratacion.contratacion_tipo == contratacion_tipo)
            if not tipo_contratacion_encontrada:
                print("No existe el tipo de contratación deseado.")
                return None
            try:
                nueva_contratacion = Contratacion(
                    nro_contratacion=nro_contratacion,
                    id_contratacion_tipo=tipo_contratacion_encontrada.id,
                )
                nueva_contratacion.save()
                print("Nueva obra registrada con éxito.")
                return nueva_contratacion.id
            except Exception as e:
                print(f"No se pudo crear la contratación. Error: {e}")
                return None
        except Exception as e:
            print(f"No existe el tipo de contratacion deseado. Error: {e}")
            return None
        
    def adjudicar_obra(self, licitacion_oferta_empresa, expediente_numero):
        try:
            empresa_encontrada = Empresa.get_or_none(Empresa.licitacion_oferta_empresa == licitacion_oferta_empresa)
            if empresa_encontrada:
                    print(f"La empresa se encontró correctamente ")
            return empresa_encontrada.id, expediente_numero
        except Exception as e:
            print(f"Error: {e}")
        
    def iniciar_obra(mano_obra, destacada, fecha_inicio, fecha_fin_inicial, fuente_financiamiento ):
        try:
            fuente_financiamiento_encontrada = FuenteFinanciamiento.get_or_none(FuenteFinanciamiento.financiamiento == fuente_financiamiento)
            if not fuente_financiamiento_encontrada:
                print("No existe esa fuente de financiamiento.")
                return None
            return fuente_financiamiento_encontrada.id, destacada, fecha_inicio,fecha_fin_inicial
        except Exception as e:
            print(f"Error: {e}")
            return None

    def actualizar_porcentaje_avance(self, porcentaje_avance):
        if 0 <= porcentaje_avance <= 100:
            self.porcentaje_avance = porcentaje_avance
            print(f"Porcentaje de avance actualizado a {porcentaje_avance}%.")
        else:
            raise ValueError("El porcentaje debe estar entre 0 y 100.")
        print("Porcentaje de avance correcto")
        return porcentaje_avance


    def incrementar_plazo(self, plazo):
        if plazo <= 0:
            print("El plazo debe ser un número positivo.")
            return False
        else:
            try:
                self.plazo_meses+= plazo
                print(f"Se incrementó el plazo de la obra en {plazo}. Total actual: {self.plazo_meses}.")
                return True
            except Exception as e:
                print(f"No se pudo incrementar el plazo. Error: {e}")
                return False

    def incrementar_mano_obra(self, mano_obra) -> bool:
        if mano_obra <= 0:
            print("La mano obra debe ser un número positivo.")
            return False
        else:
            try:
                self.mano_obra += mano_obra # incrementa la mano de obra
                print(f"Se incrementó la mano de obra en {mano_obra}. Total actual: {self.mano_obra}.")
                return True
            except Exception as e:
                print(f"No se pudo incrementar la mano obra. Error: {e}")
                return False


    def finalizar_obra(self):
        try:
            etapa_finalizada, created = Etapa.get_or_create(Etapa.etapa == 'Finalizada')
            if created:
                print('Se creo la etapa Finalizada en la base de datos...')
            else:
                print('Se encontro la etapa Finalizada en la base de datos...')
            self.id_etapas = etapa_finalizada.id
            self.porcentaje_avance = 100
            print('Etapa Finalizada con exito.')
            return True
        except Exception as e:
            print(f"No se pudo finalizar la obra. Error: {e}")
            return False
    
    def rescindir_obra(self) -> bool:
        try:
            etapa_rescindida, created = Etapa.get_or_create(Etapa.etapa == 'Rescindida')
            if created:
                print('Se creo la etapa Rescindida en la base de datos...')
            else:
                print('Se encontro la etapa Rescindida en la base de datos...')
            self.id_etapas = etapa_rescindida.id
            print('Etapa Rescindida con exito.')
            return True
        except Exception as e:
            print(f"No se pudo rescindir la obra. Error: {e}")
            return False
