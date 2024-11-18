import pandas as pd
from peewee import *
from modelo_orm import *
from abc import ABC, abstractmethod
from modelo_orm import *
class GestionarObra(ABC):
    def __init__(self):
        super().__init__()
    
    @classmethod
    @abstractmethod
    def limpiar_datos(cls, df: pd.DataFrame) -> pd.DataFrame:
       pass

    def extraer_datos():
        """que debe incluir las sentencias necesarias para manipular el dataset a
través de un objeto Dataframe del módulo “pandas”."""
        pass

    def conectar_db():
        """que debe incluir las sentencias necesarias para realizar la conexión a la base de datos “obras_urbanas.db”."""
        pass

    def mapear_orm():
        sqlite_db.init('obras_urbanas.db') 
        sqlite_db.connect()
        try:
            sqlite_db.create_tables([Obra
                            ,Area
                            ,FuenteFinanciamiento
                            ,Comuna
                            ,Etapa
                            ,Licitacion
                            ,TipoContratacion
                            ,Contratacion
                            ,TipoObra
                            ,Relacion])  # no problems.
        except Exception as e:
            print(f'El error de peewee: {e}')
            sqlite_db.close()

    def cargar_datos(df):
        for index, row in df.iterrows():
            obra = Obra.create(
                nombre=row['nombre'],
                descripcion=row['descripcion'],
                expediente_numero=row['expediente_numero'],
                mano_obra=row['mano_obra'],
                destacada=row['destacada'],
                fecha_inicio=row['fecha_inicio'],
                fecha_fin_inicial=row['fecha_fin_inicial'],
                plazo_meses=row['plazo_meses']
            )

            comuna = Comuna.create(
                barrio=row['barrio'],
                comuna=row['comuna']
            )

            area = Area.create(
                area_responsable=row['area_responsable']
            )

            fuente_financiamiento = FuenteFinanciamiento.create(
                financiamiento=row['financiamiento']
            )

            tipo_obra = TipoObra.create(
                tipo=row['tipo']
            )

            etapa = Etapa.create(
                etapa=row['etapa'],
                porcentaje_avance=row['porcentaje_avance']
            )

            licitacion = Licitacion.create(
                licitacion_oferta_empresa=row['licitacion_oferta_empresa'],
                monto_contrato=row['monto_contrato']
            )

            tipo_contratacion = TipoContratacion.create(
                contratacion_tipo=row['contratacion_tipo']
            )

            contratacion = Contratacion.create(
                nro_contratacion=row['nro_contratacion'],
                id_contratacion_tipo=tipo_contratacion
            )

            Relacion.create(
                id_obras=obra,
                id_comuna=comuna,
                id_area_responsable=area,
                id_tipo=tipo_obra,
                id_financiamiento=fuente_financiamiento,
                id_contratacion=contratacion,
                id_etapas=etapa,
                id_licitaciones=licitacion
            )
            print("Datos cargados exitosamente.")
            
    def nueva_obra():
        try:
            nombre = input("Nombre de la obra: ")
            descripcion = input("Ingrese la descripción de la obra: ")
            expediente_numero = input("Ingrese el número de expediente")
            mano_obra = int(input("Ingrese cantidad de mano de obra: "))
            fecha_inicio = input("Fecha de inicio (YYYY-MM-DD): ")
            fecha_fin_inicial = input("Fecha de fin (YYYY-MM-DD, opcional): ")
            destacada = input("Ingrese si es destacada: ")
            plazo_meses = int(input("Ingrese la cantidad de meses que durarà la obra: "))
            
            nueva_obra = Obra(
                nombre_obra=nombre,
                descripcion=descripcion,
                expediente_numero=expediente_numero,
                fecha_inicio=fecha_inicio,
                fecha_fin_inicial=fecha_fin_inicial if fecha_fin_inicial else None,
                mano_obra=mano_obra,
                destacada=destacada,
                plazo_meses=plazo_meses
            )
            nueva_obra.save()
            print("Nueva obra registrada con éxito.")
            return nueva_obra

        except DoesNotExist:
            print("La categoría ingresada no existe.")
        except Exception as e:
            print(f"Error: {e}")

    def obtener_listado_areas_responsables():
        try:
            query = (Area
            .select(Area.area_responsable)
            .distinct())
        except Exception as e:
            print(f'El error de peewee: {e}')

    def obtener_listado_tipos_obra():
        try:
            query = (TipoObra
                     .select(TipoObra.tipo))
        except Exception as e:
            print(f'El error de peewee: {e}')

    def obtener_cantidad_obras_por_etapa():
        try: 
            query = (
            Relacion
            .select(fn.COUNT(Relacion.id).alias('cantidad_obras'), Etapa.etapa)
            .join(Etapa, on=(Relacion.id_etapas == Etapa.id))
            .group_by(Etapa.etapa)
            )
        except Exception as e:
            print(f'El error de peewee: {e}')
    
    def obtener_cantidad_obras_monto_por_obra():
        try:
            query = (
            Relacion
            .select(
            fn.COUNT(Obra.id).alias('cantidad_obras'),
            Obra.name.alias('nombre_obra'),
            Licitacion.monto_contrato.alias('monto_contrato')
            )   
            .join(Obra, on=(Relacion.id_obras == Obra.id))
            .join(Licitacion, on=(Relaciones.id_licitaciones == Licitacion.id)))
        except Exception as e:
            print(f'El error de peewee: {e}')
    
    def obtener_barrios_por_comuna():
        try:
            query1 = (
            Comuna
            .select(Comuna.barrio)
            .where(Comuna.comuna == 1)
            )
            query2 = (
            Comuna
            .select(Comuna.barrio)
            .where(Comuna.comuna == 2)
            )
            query3 = (
            Comuna
            .select(Comuna.barrio)
            .where(Comuna.comuna == 3)
            )
        except Exception as e:
            print(f'El error de peewee: {e}')
    
    def obtener_cantidad_obras_finalizadas_monto_total_comuna1():
        try:
            query = (
            Relacion
            .select(fn.COUNT(Obra.id).alias('cantidad_obras'), fn.Sum(Licitacion.monto_contrato))
            .where(Etapa.etapa == 'finalizada')   
            .join(Obra, on=(Relacion.id_obras == Obra.id))
            .join(Etapa, on=(Relacion.id_etapas == Etapa.id))
            .join(Licitacion, on=(Relacion.id_licitaciones == Licitacion.id)))
        except Exception as e:
            print(f'El error de peewee: {e}')

    def obtener_cantidad_obras_finalizadas_menos_24_meses():
        try:
            query=(
            Relaciones
            .select(fn.COUNT(Obras.id).alias('cantidad_obras'))
            .join(Obras, on=(Relaciones.id_obras == Obras.id))
            .join(Etapas, on=(Relaciones.id_etapas == Etapas.id))
            .where((Etapas.etapa == 'finalizada') & (Obras.plazo_meses < 24))
            )
        except peewee.IntegrityError as e:
            print(f'El error de peewee: {e}')
    
    # tengo dudas sobre este. Y me falta poner el fetchall o for en cada parte para que me haga un print
    def obtener_porcentaje_obras_finalizadas(): 
        try:
            query=(
            Relacion
            .select(
            (fn.COUNT(Relacion.id) / fn.COUNT(
            Relacion
            .select()
            .join(Obra, on=(Relacion.id_obras == Obra.id))
            .join(Etapa, on=(Relacion.id_etapas == Etapa.id))
            .where(Etapa.etapa == 'finalizada')
            ) * 100).alias('porcentaje_finalizadas')
            )
            )
        except Exception as e:
            print(f'El error de peewee: {e}')
        
    def obtener_cantidad_total_mano_obra():
        try:
            query=(
            Obra
            .select(fn.Sum(Obra.mano_obra)
            )
            )
        except Exception as e:
            print(f'El error de peewee: {e}')

    def obtener_monto_total_inversion():
        try:
            query=(
            Licitacion
            .select(fn.Sum(Licitacion.monto_contrato)
            )
            )
        except Exception as e:
            print(f'El error de peewee: {e}')


    def obtener_indicadores():
       GestionarObra.obtener_listado_areas_responsables()
       GestionarObra.obtener_listado_tipos_obra()
       GestionarObra.obtener_cantidad_obras_por_etapa()
       GestionarObra.obtener_cantidad_obras_monto_por_obra()
       GestionarObra.obtener_obtener_barrios_por_comuna()
       GestionarObra.obtener_cantidad_obras_finalizadas_monto_total_comuna1()
       GestionarObra.obtener_cantidad_obras_finalizadas_menos_24_meses()
       GestionarObra.obtener_porcentaje_obras_finalizadas()
       GestionarObra.obtener_cantidad_total_mano_obra()
       GestionarObra.obtener_monto_total_inversion()