from gestionar_obras import *

class ObrasConstruccion(GestionarObra):
    @classmethod
    def extraer_datos(cls):
        archivo_csv = "./observatorio-de-obras-urbanas.csv"
        try:
            df = pd.read_csv(archivo_csv, sep=";", encoding='latin1')
            columnas_a_eliminar = [
                'entorno', 'direccion', 'lat', 'lng', 'imagen_1', 'imagen_2', 
                'imagen_3', 'imagen_4', 'licitacion_anio', 'cuit_contratista', 
                'beneficiarios', 'compromiso', 'ba_elige', 'link_interno', 
                'pliego_descarga', 'estudio_ambiental_descarga'
            ]
            df = df.drop(columns=columnas_a_eliminar, errors='ignore')
            print(f"Extracción de datos correcta")
            return df
        except FileNotFoundError as e:
            print("Error al conectar con el dataset.", e)
            return False

    @classmethod
    def conectar_db(cls):
        sqlite_db = SqliteDatabase('./obras_urbanas.db')
        try:
            sqlite_db.connect()
            print("Conexión exitosa con la base de datos.")
            return sqlite_db
        except OperationalError as e:
            print("Error al conectar con la BD.", e)
            exit()
            sqlite_db.connect()

    @classmethod
    def mapear_orm(cls)->bool:
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
            print('Tablas creadas correctamente')
            return True
        except Exception as e:
            print(f'Error: {e}')
            sqlite_db.close()
            return False

    
    @classmethod
    def limpiar_datos(cls, df: pd.DataFrame) -> pd.DataFrame:
        df = df.dropna(how='all')  
        df = df.fillna({col: 'Desconocido' if df[col].dtype == 'object' else 0 
                        for col in df.columns})
        
        if 'monto_contrato' in df.columns:
            df['monto_contrato'] = df['monto_contrato'].replace({'\$': '', '\.': '', ',': '.'}, regex=True)
        print("Datos limpios")
        return df

    @classmethod
    def cargar_datos(cls, df) -> bool:
        try:
            for index, row in df.iterrows():
                comuna = Comuna.get_or_create(comuna=row['comuna'])[0]
                barrio, _ = Barrio.get_or_create(barrio=row['barrio'], id_comuna=comuna.id)
                area = Area.get_or_create(area_responsable=row['area_responsable'])[0]
                fuente_financiamiento = FuenteFinanciamiento.get_or_create(financiamiento=row['financiamiento'])[0]
                tipo_obra = TipoObra.get_or_create(tipo=row['tipo'])[0]
                etapa = Etapa.get_or_create(etapa=row['etapa'])[0]
                empresa = Empresa.get_or_create(licitacion_oferta_empresa=row['licitacion_oferta_empresa'])[0]
                tipo_contratacion = TipoContratacion.get_or_create(contratacion_tipo=row['contratacion_tipo'])[0]
                contratacion = Contratacion.get_or_create(
                    nro_contratacion=row['nro_contratacion'], 
                    id_contratacion_tipo=tipo_contratacion.id
                )[0]
                
                obra = Obra.create(
                    nombre=row['nombre'],
                    descripcion=row['descripcion'],
                    expediente_numero=row['expediente-numero'],
                    mano_obra=row['mano_obra'],
                    destacada=row['destacada'],
                    fecha_inicio=row['fecha_inicio'],
                    fecha_fin_inicial=row['fecha_fin_inicial'],
                    plazo_meses=row['plazo_meses'],
                    monto_contrato=row['monto_contrato'],
                    porcentaje_avance=row['porcentaje_avance'],
                    id_barrio=barrio.id,
                    id_area_responsable=area.id,
                    id_tipo=tipo_obra.id,
                    id_financiamiento=fuente_financiamiento.id,
                    id_contratacion=contratacion.id,
                    id_etapas=etapa.id,
                    id_empresas=empresa.id
                )
                obra.save()

            print("Todos los datos se cargaron exitosamente.")
            return True

        except Exception as e:
            print(f"Error al cargar los datos: {e}")
            return False



    @classmethod
    def nueva_obra(cls):
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
                    tipo_encontrado= TipoObra.get_or_none(TipoObra.tipo == tipo)
                    if tipo_encontrado is None:
                        print(f"El tipo de obra ingresado no existe")
                    else:
                        break
                except Exception as e:
                    print(f"Error: {e}")            

            nro_contratacion = input("Ingrese el número de contratación: ")
            while True:
                contratacion_tipo = input("Ingrese el tipo de contratación: ")
                contratacion, id_contratacion= Obra.iniciar_contratacion(nro_contratacion, contratacion_tipo)
                if contratacion:
                    break

            expediente_numero = input("Ingrese el número de expediente")
            while True:
                licitacion_oferta_empresa = input("Ingrese la empresa adjudicada: ")
                empresa, id_empresa= Obra.adjudicar_obra(licitacion_oferta_empresa)
                if empresa:
                    break

            etapa, id_etapa= Obra.nuevo_proyecto()
            
            mano_obra = int(input("Ingrese cantidad de mano de obra: "))
            destacada = input("Ingrese si es destacada: ")
            fecha_inicio = input("Fecha de inicio (YYYY-MM-DD): ")
            fecha_fin_inicial = input("Fecha de fin (YYYY-MM-DD, opcional): ")
            while True:
                financiamiento = input("Ingrese la fuente de financiamiento: ")
                inicio_obra, id_inicio_obra= Obra.iniciar_obra(financiamiento)
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
                id_contratacion = id_contratacion,
                id_empresas= id_empresa,
                id_etapas = id_etapa,
                id_financiamiento =id_inicio_obra,
                id_barrio= barrio_encontrado.id   
            )
            ObraGuardada = nueva_obra.save()
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
            print(f"Este es el resultado de listar de todas las áreas responsables: ") 
            for row in results: 
                print(f"{row.area_responsable}") 
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
            print(f"Este es el resultado de listar de todos los tipos de obra: ") 
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
                Obra
                .select(Etapa.etapa, fn.COUNT(Obra.id).alias('cantidad_obras'))
                .join(Etapa, on=(Obra.id_etapas == Etapa.id))
                .group_by(Obra.id_etapas)
            )
            results = query.execute()
            print("Este es el resultado de cantidad de obras que se encuentran en cada etapa:")
            for row in results:
                print(f"Etapa: {row.id_etapas}, Cantidad de Obras: {row.cantidad_obras}")
            return True
        except Exception as e:
            print(f'Error: {e}')
            return False
    
    @classmethod
    def obtener_cantidad_obras_monto_por_obra(cls) -> bool:
        try:
            query = (
                Obra
                .select(TipoObra.tipo, 
                        fn.COUNT(Obra.id).alias('cantidad_obras'), 
                        fn.SUM(Obra.monto_contrato).alias('monto_total'))
                .join(TipoObra, on=(Obra.id_tipo == TipoObra.id))
                .group_by(TipoObra.tipo)
            )
            print(f"Este es el resultado de Cantidad de obras y monto total de inversión por tipo de obra:")
            for row in query.dicts():
                print(f"Tipo de obra: {row['tipo']}, Cantidad de Obras: {row['cantidad_obras']}, Monto total: {row['monto_total']}")
            return True
        except Exception as e:
            print(f'Error: {e}')
            return False
        
    @classmethod
    def obtener_barrios_por_comunas_especificas(cls) -> bool:
        try:
            query = (
                Barrio
                .select(Barrio.barrio)
                .join(Comuna, on=(Barrio.id_comuna == Comuna.id))
                .where(Comuna.comuna.in_([1, 2, 3]))
            )
            print(f"Este es el resultado de listar todos los barrios pertenecientes a las comunas 1, 2 y 3: ")
            for row in query.dicts():
                print(f"Barrio: {row['barrio']}")
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
                Obra
                .select(fn.COUNT(Obra.id).alias('cantidad_obras'), fn.SUM(Obra.monto_contrato).alias('monto_total'))
                .join(Etapa, on=(Obra.id_etapas == Etapa.id))
                .join(Barrio, on=(Obra.id_barrio == Barrio.id))
                .join(Comuna, on=(Barrio.id_comuna == Comuna.id))
                .where((Etapa.etapa == 'finalizada') & (Comuna.comuna == 1))
            )
            result = query.dicts().first()
            print(f"Este es el resultado de Cantidad de obras finalizadas y su y monto total de inversión en la comuna 1:")
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
    def obtener_cantidad_obras_finalizadas_menos_24_meses(cls) -> bool:
        try:
            query = (
                Obra
                .select(fn.COUNT(Obra.id).alias('cantidad_obras'))
                .join(Etapa, on=(Obra.id_etapas == Etapa.id))
                .where((Etapa.etapa == 'finalizada') & (Obra.plazo_meses <= 24))
            )
            cantidad_obras = query.scalar() 
            print(f"Este es el resultado de cantidad de obras finalizadas en un plazo menor o igual a 24 meses:") 
            if cantidad_obras:
                print(f"En un plazo de 24 meses o menos se han finalizado {cantidad_obras} obras")
            else:
                print("No se han encontrado obras finalizadas en un plazo menor o igual a 24 meses.")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    @classmethod
    def obtener_porcentaje_obras_finalizadas(cls) -> bool:
        try:
            total_obras_query = Obra.select(fn.COUNT(Obra.id).alias('total_obras'))
            total_obras = total_obras_query.scalar() or 0
            finalizadas_query = (
                Obra
                .select(fn.COUNT(Obra.id).alias('obras_finalizadas'))
                .join(Etapa, on=(Obra.id_etapas == Etapa.id))
                .where(Etapa.etapa == 'finalizada')
            )
            obras_finalizadas = finalizadas_query.scalar() or 0
            print(f"Este es el resultado de Porcentaje total de obras finalizadas:")
            if total_obras > 0:
                porcentaje_finalizada = (obras_finalizadas * 100) / total_obras
                print(f"Un {porcentaje_finalizada:.2f}% de las obras se han finalizado.")
            else:
                print("No hay obras registradas.")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    
    @classmethod
    def obtener_cantidad_total_mano_obra(cls):
        try:
            query = Obra.select(fn.Sum(Obra.mano_obra).alias('total_mano_obra')).scalar()
            print(f"Este es el resultado de cantidad total de mano de obra empleada:")
            if query is not None:
                print(f"{query}")
                return True
            else:
                print(f"No hay mano de obra")
                return False
        except Exception as e:
            print(f'Error: {e}')
            return False


    @classmethod
    def obtener_monto_total_inversion(cls):
        try:
            total_inversion = Obra.select(fn.Sum(Obra.monto_contrato)).scalar()
            print(f"Este es el resultado de Monto total de inversión: ")
            if total_inversion is not None:
                print(f"{total_inversion}")
                return True
            else:
                print(f"No hay monto total de inversion")
                return False
        except Exception as e:
            print(f'Error: {e}')
            return False

    
    @classmethod
    def obtener_indicadores(cls):
       cls.obtener_listado_areas_responsables()
       cls.obtener_listado_tipos_obra()
       cls.obtener_cantidad_obras_por_etapa()
       cls.obtener_cantidad_obras_monto_por_obra()
       cls.obtener_barrios_por_comunas_especificas()
       cls.obtener_cantidad_obras_finalizadas_monto_total_comuna1()
       cls.obtener_cantidad_obras_finalizadas_menos_24_meses()
       cls.obtener_porcentaje_obras_finalizadas()
       cls.obtener_cantidad_total_mano_obra()
       cls.obtener_monto_total_inversion()