from gestionar_obras import *

class ObrasConstruccion(GestionarObra):
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
        sqlite_db =SqliteDatabase('/obras_urbanas.db', pragmas={'journal_mode': 'wal'})
        try:
            sqlite_db.connect()
        except OperationalError as e:
            print("Error al conectar con la BD.", e)
            exit()
        return sqlite_db

    @classmethod
    def mapear_orm(cls):
        sqlite_db = cls.conectar_db()
        try:
            sqlite_db.create_tables([
                            Area
                            ,FuenteFinanciamiento
                            ,Comuna
                            ,Barrio
                            ,Etapa
                            ,Empresa
                            ,TipoContratacion
                            ,Contratacion
                            ,TipoObra
                           ,Obra
                            ])  
        except Exception as e:
            print(f'Error: {e}')
            sqlite_db.close()
    
    @classmethod
    def limpiar_datos(cls, df: pd.DataFrame) -> pd.DataFrame:
        df = df.dropna(how='all')  
        df = df.fillna({col: 'Desconocido' if df[col].dtype == 'object' else 0 
            for col in df.columns})
        return df

    @classmethod
    def cargar_datos(df)->bool:
        for index, row in df.iterrows():
            try: 
                comuna = Comuna.get_or_create(
                    comuna=row['comuna']
                )
                barrio = Barrio.get_or_create(
                    barrio=row['barrio'],
                    id_comuna=comuna.id
                )

                area = Area.get_or_create(
                    area_responsable=row['area_responsable']
                )

                fuente_financiamiento = FuenteFinanciamiento.get_or_create(
                    financiamiento=row['financiamiento']
                )

                tipo_obra = TipoObra.get_or_create(
                    tipo=row['tipo']
                )

                etapa = Etapa.get_or_create(
                    etapa=row['etapa'],
                    porcentaje_avance=row['porcentaje_avance']
                )

                empresa = Empresa.get_or_create(
                    licitacion_oferta_empresa=row['licitacion_oferta_empresa'],
                    monto_contrato=row['monto_contrato']
                )

                tipo_contratacion = TipoContratacion.get_or_create(
                    contratacion_tipo=row['contratacion_tipo']
                )

                contratacion = Contratacion.get_or_create(
                    nro_contratacion=row['nro_contratacion'],
                    id_contratacion_tipo=tipo_contratacion
                )

                obra = Obra.create(
                    nombre=row['nombre'],
                    descripcion=row['descripcion'],
                    expediente_numero=row['expediente_numero'],
                    mano_obra=row['mano_obra'],
                    destacada=row['destacada'],
                    fecha_inicio=row['fecha_inicio'],
                    fecha_fin_inicial=row['fecha_fin_inicial'],
                    plazo_meses=row['plazo_meses'],
                    id_barrio=barrio.id,
                    id_area_responsable=area.id,
                    id_tipo=tipo_obra.id,
                    id_financiamiento=fuente_financiamiento.id,
                    id_contratacion=contratacion.id,
                    id_etapas=etapa.id,
                    id_empresas=empresa.id
                )
                obra.save()
                print("Datos cargados exitosamente.")
                return True
            except Exception as e:
                print(f"Error: {e}")
                return False

    @classmethod
    def nueva_obra():
        try:
            nombre = input("Ingrese el nombre de la obra: ")
            descripcion = input("Ingrese la descripción de la obra: ")
          
            plazo_meses = int(input("Ingrese la cantidad de meses que durarà la obra: "))
            monto_contrato= float(input("Ingrese el monto del contrato:"))
            
            while True:
                area_responsable = input("Ingrese el nombre del area responsable: ")
                try: 
                    area_encontrada= Area.get_or_none(Area.area_responsable == area_responsable)
                    if area_encontrada is None:
                        print(f"El area ingresada no existe")
                    else:
                        break
                except Exception as e:
                    print(f"Error: {e}")
            
            while True:
                tipo = input("Ingrese el nombre del tipo de obra: ")
                try: 
                    tipo_encontrado= Area.get_or_none(TipoObra.tipo == tipo)
                    if tipo_encontrado is None:
                        print(f"El tipo de obra ingresado no existe")
                    else:
                        break
                except Exception as e:
                    print(f"Error: {e}")            

            nro_contratacion = input("Ingrese el número de contratación: ")

            while True:
                contratacion_tipo = input("Ingrese el tipo de contratación: ")
                contratacion= Obra.iniciar_contratacion(nro_contratacion, contratacion_tipo)
                if contratacion:
                    break     

            nueva_contratacion= Contratacion(
                nro_contratacion= nro_contratacion,
                id_contratacion_tipo= contratacion_tipo_encontrado.id
            ).save()

            expediente_numero = input("Ingrese el número de expediente")
            while True:
                licitacion_oferta_empresa = input("Ingrese la empresa adjudicada: ")
                empresa= Obra.adjudicar_obra(licitacion_oferta_empresa, expediente_numero)
                if empresa:
                    break
                
            etapa= Obra.nuevo_proyecto()
            mano_obra = int(input("Ingrese cantidad de mano de obra: "))
            destacada = input("Ingrese si es destacada: ")
            fecha_inicio = input("Fecha de inicio (YYYY-MM-DD): ")
            fecha_fin_inicial = input("Fecha de fin (YYYY-MM-DD, opcional): ")
            while True:
                financiamiento = input("Ingrese la fuente de financiamiento: ")
                inicio_obra= Obra.iniciar_obra(mano_obra, destacada, fecha_inicio, fecha_fin_inicial, financiamiento)
                if inicio_obra:
                    break

            while True:
                barrio = input("Ingrese el barrio: ")
                try: 
                    barrio_encontrado= Barrio.get_or_none(Barrio.barrio == barrio)
                    if barrio_encontrado is None:
                        print(f"El barrio no existe")
                    else:
                        break
                except Exception as e:
                    print(f"Error: {e}")               
            nueva_obra = Obra(
                nombre=nombre,
                descripcion=descripcion,
                expediente_numero=expediente_numero,
                fecha_inicio=fecha_inicio,
                fecha_fin_inicial=fecha_fin_inicial if fecha_fin_inicial else None,
                mano_obra=mano_obra,
                destacada=destacada,
                plazo_meses=plazo_meses,
                monto_contrato =monto_contrato, 
                porcentaje_avance = 0,
                id_area_responsable=area_encontrada.id,
                id_tipo = tipo_encontrado.id,
                id_contratacion = nueva_contratacion.id,
                id_empresas= licitacion_oferta_empresa_encontrada.id,
                id_etapas = etapa,
                id_financiamiento =financiamiento_encontrado.id,
                id_barrio= barrio_encontrado.id   
            ).save()
            print("Nueva obra registrada con éxito.")
            return nueva_obra
        except Exception as e:
            print(f'Error: {e}')
            return False

    @classmethod
    def obtener_listado_areas_responsables(cls) -> bool:
        try:
            query = (Area
            .select(Area.area_responsable))
            results = query.execute() 
            for row in results: 
                print(row.area_responsable) 
            return True 
        except Exception as e:
            print(f'Error: {e}')
            return False

    @classmethod
    def obtener_listado_tipos_obra(cls) -> bool:
        try:
            query = (TipoObra
                     .select(TipoObra.tipo))
            results = query.execute() 
            for row in results: 
                print(row.tipo) 
            return True 
        except Exception as e:
            print(f'Error: {e}')
            return False

    @classmethod
    def obtener_cantidad_obras_por_etapa(cls) -> bool:
        try:
            query = (
                Relacion
                .select(fn.COUNT(Relacion.id).alias('cantidad_obras'), Etapa.etapa)
                .join(Etapa, on=(Relacion.id_etapas == Etapa.id))
                .group_by(Etapa.etapa)
            )
            results = query.execute()
            for row in results:
                print(f"Etapa: {row.etapa}, Cantidad de Obras: {row.cantidad_obras}")
            return True
        except Exception as e:
            print(f'Error: {e}')
            return False
    
    @classmethod
    def obtener_cantidad_obras_monto_por_obra(cls) -> bool:
        try:
            query = (
                Relacion
                .select(
                    fn.COUNT(Obra.id).alias('cantidad_obras'),
                    Obra.name.alias('nombre_obra'),
                    Empresa.monto_contrato.alias('monto_contrato')
                )
                .join(Obra, on=(Relacion.id_obras == Obra.id))
                .join(Empresa, on=(Relacion.id_empresas == Empresa.id))
                .group_by(Obra.name, Empresa.monto_contrato)
            )
            
            for row in query.dicts():
                print(f"Cantidad de obras: {row['cantidad_obras']}, "
                    f"Nombre de la obra: {row['nombre_obra']}, "
                    f"Monto del contrato: {row['monto_contrato']}")
            return True
        except Exception as e:
            print(f'Error: {e}')
            return False

    @classmethod
    def obtener_barrios_por_comunas_especificas(cls) -> bool:
        try:
            comunas_ids = [1, 2, 3]

            query = (Barrio
                    .select(Comuna.comuna, Barrio.barrio)
                    .join(Comuna)
                    .where(Comuna.id.in_(comunas_ids))
                    .dicts())  

            resultado = {}
            for fila in query:
                comuna = fila['comuna']
                barrio = fila['barrio']
                if comuna not in resultado:
                    resultado[comuna] = []
                resultado[comuna].append(barrio)

            if resultado:
                for comuna, barrios in resultado.items():
                    print(f"Comuna: {comuna}")
                    for barrio in barrios:
                        print(f"  - {barrio}")
                return True
            else:
                print("No se encontraron barrios para las comunas solicitadas.")
                return False
        except Exception as e:
            print(f'Error: {e}')
            return False

    @classmethod
    def obtener_cantidad_obras_finalizadas_monto_total_comuna1(cls) -> bool:
        try:
            query = (
                Relacion
                .select(fn.COUNT(Obra.id).alias('cantidad_obras'), fn.SUM(Empresa.monto_contrato).alias('monto_total'))
                .where(Etapa.etapa == 'finalizada')   
                .join(Obra, on=(Relacion.id_obras == Obra.id))
                .join(Etapa, on=(Relacion.id_etapas == Etapa.id))
                .join(Empresa, on=(Relacion.id_empresas == Empresa.id))
            )

            result = query.dicts().first()
            
            if result:
                cantidad_obras = result['cantidad_obras']
                monto_total = result['monto_total'] or 0.0
                print(f'Cantidad de obras finalizadas: {cantidad_obras}')
                print(f'Monto total de contratos: {monto_total}')
                return True
            else:
                print('No se encontraron obras finalizadas.')
                return False
        
        except Exception as e:
            print(f'Error: {e}')
            return False

    
    @classmethod
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

    @classmethod
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
    
    @classmethod
    def obtener_cantidad_total_mano_obra():
        try:
            query=(
            Obra
            .select(fn.Sum(Obra.mano_obra)
            )
            )
        except Exception as e:
            print(f'El error de peewee: {e}')

    @classmethod
    def obtener_monto_total_inversion():
        try:
            query=(
            Empresa
            .select(fn.Sum(Empresa.monto_contrato)
            )
            )
        except Exception as e:
            print(f'El error de peewee: {e}')
    
    @classmethod
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