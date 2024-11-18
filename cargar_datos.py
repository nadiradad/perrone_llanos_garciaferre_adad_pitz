import pandas as pd

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
