from gestionar_obras import *

class ObrasConstruccion(GestionarObra):
    
    @classmethod
    def limpiar_datos(cls, df: pd.DataFrame) -> pd.DataFrame:
        df = df.dropna(how='all')  
        df = df.fillna({col: 'Desconocido' if df[col].dtype == 'object' else 0 
            for col in df.columns})
        return df
    
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