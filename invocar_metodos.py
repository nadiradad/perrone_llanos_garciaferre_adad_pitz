from ObrasConstruccion import *
ObrasConstruccion.conectar_db()
ObrasConstruccion.mapear_orm()
df= ObrasConstruccion.extraer_datos()
ObrasConstruccion.limpiar_datos(df)
ObrasConstruccion.cargar_datos(df)
ObrasConstruccion.obtener_indicadores()
obra1 =ObrasConstruccion.nueva_obra()
porcentaje = 20
obra1.actualizar_porcentaje_avance(porcentaje)
manoObra=150
obra1.incrementar_mano_obra(manoObra)
obra1.finalizar_obra()
obra2 =ObrasConstruccion.nueva_obra()
porcentaje1 = 36
obra2.actualizar_porcentaje_avance(porcentaje1)
manoObra1=231
obra2.incrementar_mano_obra(manoObra1)
obra2.rescindir_obra()