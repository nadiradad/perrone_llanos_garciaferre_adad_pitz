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
    def nuevo_proyecto(self, nombre, descripcion, expediente_numero, fecha_inicio, plazo_meses):
       try:
           self.nombre = nombre
           self.descripcion = descripcion
           self.expediente_numero = expediente_numero
           self.fecha_inicio = fecha_inicio
           self.plazo_meses = plazo_meses
           self.save()  
           print(f"Proyecto '{self.nombre}' registrado como nuevo proyecto.")
       except Exception as e:
           print(f"Error: {e}")

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
                return nueva_contratacion
            except Exception as e:
                print(f"No se pudo crear la contratación. Error: {e}")
                return None

        except Exception as e:
            print(f"No existe el tipo de contratacion deseado. Error: {e}")
            return None
        
    def adjudicar_obra(self, licitacion_oferta_empresa, expediente_numero):
        try:
            empresa = Empresa.get_or_none(Empresa.licitacion_oferta_empresa == licitacion_oferta_empresa)
            if empresa:
                relacion = Relacion.get_or_none(Relacion.id_empresas == empresa.id, Relacion.id_obras == self.id)
                if relacion:
                    self.licitacion_oferta_empresa = licitacion_oferta_empresa
                    self.expediente_numero = expediente_numero
                    self.save()
                    print(f"Obra {self.nombre} adjudicada exitosamente con la licitación {licitacion_oferta_empresa}.")
                else:
                    print(f"No existe una relación válida entre la obra {self.nombre} y la empresa.")
            else:
                print(f"La empresa con la licitación {licitacion_oferta_empresa} no existe.")
        except Exception as e:
            print(f"Error: {e}")
        
    def iniciar_obra(nombre, descripcion, mano_obra, destacada, fecha_inicio, fecha_fin_inicial, fuente_financiamiento ):
        try:
            fuente_financiamiento_encontrada = FuenteFinanciamiento.get_or_none(FuenteFinanciamiento.financiamiento == fuente_financiamiento)
            if not fuente_financiamiento_encontrada:
                print("No existe esa fuente de financiamiento.")
                return None
            try:
                nueva_obra = Obra(
                    nombre=nombre,
                    descripcion=descripcion,
                    destacada=destacada,
                    mano_obra=mano_obra,
                    fecha_inicio = fecha_inicio, 
                    fecha_fin_inicial =fecha_fin_inicial, 
                    financiamiento=fuente_financiamiento_encontrada.id,
                )
                nueva_obra.save()
                print("Nueva obra registrada con éxito.")
                return nueva_obra
            except Exception as e:
                print(f"No se pudo crear la contratación. Error: {e}")
                return None
        except Exception as e:
            print(f"No existe el tipo de contratacion deseado. Error: {e}")
            return None

    def actualizar_porcentaje_avance():
        pass

    def incrementar_plazo(self, nuevo_plazo, nombre_obra):
        try:
            if nuevo_plazo <= 0:
                print("El plazo debe ser un número positivo.")
                return None
        except ValueError:
            print("Debe ingresar un número entero válido.")
            return None

        try:
            obra = Obra.get_or_none(Obra.nombre == nombre_obra)
            if not obra:
                print("No existe la obra deseada.")
                return None

            obra.plazo_meses = nuevo_plazo
            obra.save()
            print(f"El plazo de la obra '{nombre_obra}' ha sido actualizado a {nuevo_plazo} meses.")
        except Exception as e:
            print(f"No se pudo modificar el plazo. Error: {e}")

    def incrementar_mano_obra():
        pass

    def finalizar_obra(self, Id):
        try:
            query = (Etapa.update(etapa='Finalizada', porcentaje_avance=100) # REEVEER! OJO CON porcentaje_avance QUE PERTENECE A OBRA
                     .where(Obra.id == Id)
                     .join(Relacion, on=(Etapa.id == Relacion.id_etapas))
                     .join(Obra, on=(Relacion.id_obras == Obra.id)))  

            rows_updated = query.execute()
            if rows_updated == 0:
                mensaje = f"No se encontró una obra con el ID {Id}."
                print(mensaje)
                return False
            else:
                mensaje = f"La obra con ID {Id} ha sido finalizada correctamente."
                print(mensaje)
                return True  
        except ValueError:
            mensaje = "El ID ingresado no es válido. Por favor, ingrese un número entero."
            print(mensaje)
            return False  
        except Exception as e:
            mensaje = f"Se produjo un error al intentar finalizar la obra: {e}"
            print(mensaje)
            return False
    
    def rescindir_obra(self,Id):
        try:
            obra_encontrada = Obra.get_or_none(Obra.id == Id)    
            if not obra_encontrada:
                print("No existe una obra con ese Id")
                return None
            try:
                obra_rescindida = Etapa.update(Etapa.etapa == 'Rescindida').where(Obra.id == Id).join(Relacion, on=(Etapa.id == Relacion.id_etapas)).join(Obra, on=(Relacion.id_obras == Obra.id))
                obra_rescindida.save()
                print("Nueva obra registrada con éxito.")
                return obra_rescindida
            except Exception as e:
                print(f"No se pudo rescindir la obra. Error: {e}")
                return None
        except Exception as e:
            print(f"Ha ocurrido un error al intentar buscar una obra con ese id. Error: {e}")
            return None

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

class Relacion(BaseModel):
    id = AutoField(primary_key=True)
    id_obras = ForeignKeyField(Obra, backref='Relaciones')
    id_barrio = ForeignKeyField(Barrio, backref='Relaciones')
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