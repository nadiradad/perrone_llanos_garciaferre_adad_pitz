from abc import ABC

class GestionarObra(ABC):
    def __init__(self):
        super().__init__()

    def extraer_datos():
        """que debe incluir las sentencias necesarias para manipular el dataset a
través de un objeto Dataframe del módulo “pandas”."""
        pass

    def conectar_db():
        """que debe incluir las sentencias necesarias para realizar la conexión a la base de datos “obras_urbanas.db”."""
        pass

    def mapear_orm():
        sqlite_db.init('obras_urbanas.db')  # database is now initialized NO SE SI ES NECESARIO
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
        except peewee.IntegrityError as e:
            print(f'El error de peewee: {e}')
            sqlite_db.close()

    def limpiar_datos():
        """que debe incluir las sentencias necesarias para realizar la “limpieza” de los datos nulos y no accesibles del Dataframe."""
        pass

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
        """que debe incluir las sentencias necesarias para crear nuevas instancias de Obra. Se deben considerar los siguientes requisitos:
        • Todos los valores requeridos para la creación de estas nuevas instancias deben ser ingresados por teclado.
        • Para los valores correspondientes a registros de tablas relacionadas (foreign key), el valor ingresado debe buscarse en la tabla correspondiente mediante sentencia de búsqueda ORM, para obtener la instancia relacionada, si el valor ingresado no existe en la tabla, se le debe informar al usuario y solicitarle un nuevo ingreso por teclado.
        • Para persistir en la BD los datos de la nueva instancia de Obra debe usarse el método save() de Model del módulo “peewee”. 
        • Este método debe retornar la nueva instancia de obra."""
        pass

    def obtener_listado_areas_responsables():
        try:
            query = (Areas
            .select(Areas.area_responsable)
            .distinct())
        except peewee.IntegrityError as e:
            print(f'El error de peewee: {e}')

    def obtener_listado_tipos_obra():
        try:
            query = (TipoObras
                     .select tipo)
        except peewee.IntegrityError as e:
            print(f'El error de peewee: {e}')

    def obtener_cantidad_obras_por_etapa():
        try: 
            query = (
            Relaciones
            .select(fn.COUNT(Relaciones.id).alias('cantidad_obras'), Etapas.etapa)
            .join(Etapas, on=(Relaciones.id_etapas == Etapas.id))
            .group_by(Etapas.etapa)
            )
        except peewee.IntegrityError as e:
            print(f'El error de peewee: {e}')
    
    def obtener_cantidad_obras_monto_por_obra():
        try:
            query = (
            Relaciones
            .select(
            fn.COUNT(Obras.id).alias('cantidad_obras'),
            Obras.name.alias('nombre_obra'),
            Licitaciones.monto_contrato.alias('monto_contrato')
            )   
            .join(Obras, on=(Relaciones.id_obras == Obras.id))
            .join(Licitaciones, on=(Relaciones.id_licitaciones == Licitaciones.id)))
        except peewee.IntegrityError as e:
            print(f'El error de peewee: {e}')
    
    def obtener_barrios_por_comuna():
        try:
            query1 = (
            Comunas
            .select(Comunas.barrio)
            .where(Comunas.comuna == 1)
            )
            query2 = (
            Comunas
            .select(Comunas.barrio)
            .where(Comunas.comuna == 2)
            )
            query3 = (
            Comunas
            .select(Comunas.barrio)
            .where(Comunas.comuna == 3)
            )
        except peewee.IntegrityError as e:
            print(f'El error de peewee: {e}')
    
    def obtener_cantidad_obras_finalizadas_monto_total_comuna1():
        try:
            query = (
            Relaciones
            .select(fn.COUNT(Obras.id).alias('cantidad_obras'), fn.Sum(Licitaciones.monto_contrato))
            .where(Etapas.etapa == 'finalizada')   
            .join(Obras, on=(Relaciones.id_obras == Obras.id))
            .join(Etapas, on=(Relaciones.id_etapas == Etapas.id))
            .join(Licitaciones, on=(Relaciones.id_licitaciones == Licitaciones.id)))
        except peewee.IntegrityError as e:
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
            Relaciones
            .select(
            (fn.COUNT(Relaciones.id) / fn.COUNT(
            Relaciones
            .select()
            .join(Obras, on=(Relaciones.id_obras == Obras.id))
            .join(Etapas, on=(Relaciones.id_etapas == Etapas.id))
            .where(Etapas.etapa == 'finalizada')
            ) * 100).alias('porcentaje_finalizadas')
            )
            )
        except peewee.IntegrityError as e:
            print(f'El error de peewee: {e}')
        
    def obtener_cantidad_total_mano_obra():
        try:
            query=(
            Obras
            .select(fn.Sum(Obras.mano_obra)
            )
            )
        except peewee.IntegrityError as e:
            print(f'El error de peewee: {e}')

    def obtener_monto_total_inversion():
        try:
            query=(
            Licitacion
            .select(fn.Sum(Licitacion.monto_contrato)
            )
            )
        except peewee.IntegrityError as e:
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