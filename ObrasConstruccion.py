from gestionar_obras import *

class ObrasConstruccion(GestionarObra):
    
    @classmethod
    def limpiar_datos(cls, df: pd.DataFrame) -> pd.DataFrame:
        df = df.dropna(how='all')  
        df = df.fillna({col: 'Desconocido' if df[col].dtype == 'object' else 0 
            for col in df.columns})
        return df
    
    @classmethod
    def extraer_datos():
        archivo_csv = "/observatorio-de-obras-urbanas.csv"
    
        try:
            df = pd.read_csv(archivo_csv, sep=",")
            return df
        except FileNotFoundError as e:
            print("Error al conectar con el dataset.", e)
            return False

    @classmethod
    def conectar_db():
        sqlite_db.init('obras_urbanas.db') 
        sqlite_db.connect()

    @classmethod
    def mapear_orm():
        try:
            sqlite_db.create_tables([Obra
                            ,Area
                            ,FuenteFinanciamiento
                            ,Comuna
                            ,Etapa
                            ,Empresa
                            ,TipoContratacion
                            ,Contratacion
                            ,TipoObra
                            ,Relacion])  # no problems.
        except Exception as e:
            print(f'El error de peewee: {e}')
            sqlite_db.close()

    @classmethod
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

            empresa = Empresa.create(
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
                id_empresas=empresa
            )
            print("Datos cargados exitosamente.")

    @classmethod
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

    @classmethod
    def obtener_listado_areas_responsables():
        try:
            query = (Area
            .select(Area.area_responsable)
            .distinct())
        except Exception as e:
            print(f'El error de peewee: {e}')

    @classmethod
    def obtener_listado_tipos_obra():
        try:
            query = (TipoObra
                     .select(TipoObra.tipo))
        except Exception as e:
            print(f'El error de peewee: {e}')

    @classmethod
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