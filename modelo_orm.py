from peewee import *

sqlite_db = SqliteDatabase('./obras_urbanas.db')
try:
    sqlite_db.connect()
    print("Conexión exitosa con la base de datos.")
except OperationalError as e:
    print("Error al conectar con la BD:", e)
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
    comuna = IntegerField(null=True)
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
    mano_obra = IntegerField(null=True)
    destacada = CharField(max_length=2)
    fecha_inicio = DateField(null=True)
    fecha_fin_inicial = DateField(null=True)
    plazo_meses = IntegerField(null=True)
    monto_contrato = FloatField(null=True)
    porcentaje_avance = IntegerField(null=True)
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
    def nuevo_proyecto()->bool:
       try:
           etapa_encontrada, created= Etapa.get_or_create(etapa = 'Proyecto')
           if created == True:
               print(f"La etapa proyecto no existía y se ha creado en la bbdd")
           else:
                print(f"Etapa del proyecto encontrada")
           print("nuevo proyecto iniciado correctamente")
           return True, etapa_encontrada.id
       except Exception as e:
           print(f"Error: {e}")
           return False

    def iniciar_contratacion(nro_contratacion, contratacion_tipo)->bool:
        try:
            tipo_contratacion_encontrada = TipoContratacion.get(TipoContratacion.contratacion_tipo == contratacion_tipo)
            if not tipo_contratacion_encontrada:
                print(f"No se ha encontrado el tipo de contratación solicitada")
                return False
            else:
                nueva_contratacion = Contratacion(nro_contratacion=nro_contratacion,
                                                  id_contratacion_tipo=tipo_contratacion_encontrada.id)
                nueva_contratacion.save()
                print(f"contratación iniciada correctamente")
                return True, tipo_contratacion_encontrada.id
        except Exception as e:
            print(f"No existe el tipo de contratacion deseado. Error: {e}")
            return None
        
    def adjudicar_obra(licitacion_oferta_empresa)->bool:
        try:
            empresa_encontrada = Empresa.get(Empresa.licitacion_oferta_empresa == licitacion_oferta_empresa)
            if not empresa_encontrada:
                print(f"La empresa solicitada no existe ")
                return False
            else:
                print("Empresa encontrada")
                return True, empresa_encontrada.id
        except Exception as e:
            print(f"Error: {e}")
        
    def iniciar_obra(fuente_financiamiento)->bool:
        try:
            fuente_financiamiento_encontrada = FuenteFinanciamiento.get(FuenteFinanciamiento.financiamiento == fuente_financiamiento)
            if not fuente_financiamiento_encontrada:
                print("No existe esa fuente de financiamiento.")
                return False
            else:
                print(f"Fuente financiamiento encontrada")
                return True, fuente_financiamiento_encontrada.id
        except Exception as e:
            print(f"Error: {e}")

    def actualizar_porcentaje_avance(self, porcentaje_avance)->bool:
        if 0 <= porcentaje_avance <= 100:
            self.porcentaje_avance = porcentaje_avance
            print(f"Porcentaje de avance actualizado a {porcentaje_avance}%.")
            return True
        else:
            raise ValueError("El porcentaje debe estar entre 0 y 100.")
            return False


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
                self.mano_obra += mano_obra
                print(f"Se incrementó la mano de obra en {mano_obra}. Total actual: {self.mano_obra}.")
                return True
            except Exception as e:
                print(f"No se pudo incrementar la mano obra. Error: {e}")
                return False


    def finalizar_obra(self):
        try:
            etapa_finalizada, created = Etapa.get_or_create(etapa = 'Finalizada')
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
            etapa_rescindida, created = Etapa.get_or_create(etapa = 'Rescindida')
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


