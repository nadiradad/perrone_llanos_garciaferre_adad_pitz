from ObrasConstruccion import *
ObrasConstruccion.conectar_db()
ObrasConstruccion.mapear_orm()
df= ObrasConstruccion.extraer_datos()
ObrasConstruccion.limpiar_datos(df)
ObrasConstruccion.cargar_datos(df)
ObrasConstruccion.obtener_indicadores()
obra1 =ObrasConstruccion.nueva_obra()
# obra1= ObrasConstruccion.nueva_obra()
# obra2 =GestionarObra.nueva_obra()
# sqlite_db.create_tables([Area, FuenteFinanciamiento, Comuna,Barrio, Etapa, Empresa, TipoContratacion, Contratacion, TipoObra,  Obra ])