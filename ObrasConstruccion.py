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
            sqlite_db.create_tables([Obra
                            ,Area
                            ,FuenteFinanciamiento
                            ,Comuna
                            ,Etapa
                            ,Empresa
                            ,TipoContratacion
                            ,Contratacion
                            ,TipoObra
                            ,Relacion])  
        except Exception as e:
            print(f'El error de peewee: {e}')
            sqlite_db.close()
    
    @classmethod
    def limpiar_datos(cls, df: pd.DataFrame) -> pd.DataFrame:
        df = df.dropna(how='all')  
        df = df.fillna({col: 'Desconocido' if df[col].dtype == 'object' else 0 
            for col in df.columns})
        return df

    @classmethod
    def cargar_datos(df):
        for index, row in df.iterrows():
            try: 
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
            except Exception as e:
                print(f"Error: {e}")
        print("Datos cargados exitosamente.")

    @classmethod
    def nueva_obra():
        try:
            nombre = input("Ingrese el nombre de la obra: ")
            descripcion = input("Ingrese la descripción de la obra: ")
            expediente_numero = input("Ingrese el número de expediente")
            mano_obra = int(input("Ingrese cantidad de mano de obra: "))
            destacada = input("Ingrese si es destacada: ")
            fecha_inicio = input("Fecha de inicio (YYYY-MM-DD): ")
            fecha_fin_inicial = input("Fecha de fin (YYYY-MM-DD, opcional): ")
            plazo_meses = int(input("Ingrese la cantidad de meses que durarà la obra: "))
            monto_contrato= float(input("Ingrese el monto del contrato:"))
            
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
                porcentaje_avance = 0   
            ).save()
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
                try: 
                    contratacion_tipo_encontrado= TipoContratacion.get_or_none(TipoContratacion.contratacion_tipo == contratacion_tipo)
                    if contratacion_tipo_encontrado is None:
                        print(f"El tipo de contratación ingresado no existe")
                    else:
                        break
                except Exception as e:
                    print(f"Error: {e}")         

            nueva_contratacion= Contratacion(
                nro_contratacion= nro_contratacion,
                id_contratacion_tipo= contratacion_tipo_encontrado.id
            ).save()

            while True:
                licitacion_oferta_empresa = input("Ingrese la empresa adjudicada: ")
                try: 
                    licitacion_oferta_empresa_encontrada= Empresa.get_or_none(Empresa.licitacion_oferta_empresa == licitacion_oferta_empresa)
                    if licitacion_oferta_empresa_encontrada is None:
                        print(f"La empresa solicitada no existe")
                    else:
                        break
                except Exception as e:
                    print(f"Error: {e}") 
            try:
                etapa_encontrada = (Etapa.select(Etapa.id).where(Etapa.etapa == 'Proyecto').scalar())   
            except Exception as e:
                print(f"Error: {e}")

            while True:
                financiamiento = input("Ingrese la empresa adjudicada: ")
                try: 
                    financiamiento_encontrado= FuenteFinanciamiento.get_or_none(FuenteFinanciamiento.financiamiento == financiamiento)
                    if financiamiento_encontrado is None:
                        print(f"La fuente de financiamiento no existe")
                    else:
                        break
                except Exception as e:
                    print(f"Error: {e}")     

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
            nueva_relacion=Relacion(
                id_obras = nueva_obra.id,
                id_area_responsable=area_encontrada.id,
                id_tipo = tipo_encontrado.id,
                id_contratacion = nueva_contratacion.id,
                id_empresas= licitacion_oferta_empresa_encontrada.id,
                id_etapas = etapa_encontrada,
                id_financiamiento =financiamiento_encontrado.id,
                id_barrio= barrio_encontrado.id
            ).save()
            print("Nueva obra registrada con éxito.")
            return nueva_obra
        except Exception as e:
            print(f"Error: {e}")

    @classmethod
    def obtener_listado_areas_responsables()->bool:
        try:
            query = (Area
            .select(Area.area_responsable))
            results = query.execute() 
            for row in results: 
                print(row.area_responsable) 
            return True 
        except Exception as e:
            print(f'El error de peewee: {e}')
            return False

    @classmethod
    def obtener_listado_tipos_obra():
        try:
            query = (TipoObra
                     .select(TipoObra.tipo))
            results = query.execute() 
            for row in results: 
                print(row.tipo) 
            return True 
        except Exception as e:
            print(f'El error de peewee: {e}')
            return False

    @classmethod
    def obtener_cantidad_obras_por_etapa():
        try: 
            query = (
            Relacion
            .select(fn.COUNT(Relacion.id).alias('cantidad_obras'), Etapa.etapa)
            .join(Etapa, on=(Relacion.id_etapas == Etapa.id))
            .group_by(Etapa.etapa)
            )
            return query
        except Exception as e:
            print(f'El error de peewee: {e}')
    
    @classmethod
    def obtener_cantidad_obras_monto_por_obra():
        try:
            query = (
            Relacion
            .select(
            fn.COUNT(Obra.id).alias('cantidad_obras'),
            Obra.name.alias('nombre_obra'),
            Empresa.monto_contrato.alias('monto_contrato')
            )   
            .join(Obra, on=(Relacion.id_obras == Obra.id))
            .join(Empresa, on=(Relacion.id_empresas == Empresa.id)))
        except Exception as e:
            print(f'El error de peewee: {e}')

    @classmethod
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

    @classmethod
    def obtener_cantidad_obras_finalizadas_monto_total_comuna1():
        try:
            query = (
            Relacion
            .select(fn.COUNT(Obra.id).alias('cantidad_obras'), fn.Sum(Empresa.monto_contrato))
            .where(Etapa.etapa == 'finalizada')   
            .join(Obra, on=(Relacion.id_obras == Obra.id))
            .join(Etapa, on=(Relacion.id_etapas == Etapa.id))
            .join(Empresa, on=(Relacion.id_empresas == Empresa.id)))
        except Exception as e:
            print(f'El error de peewee: {e}')
    
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