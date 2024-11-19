def iniciar_contratacion():
    nro_contratacion = input('Ingrese el numero de contratacion: ')
    contratacion_tipo = input('Ingrese el tipo de contratacion: ')
    try:
        tipo_contratacion_encontrada = TipoContratacion.get_or_none(TipoContratacion.contratacion_tipo == contratacion_tipo)
        
        if not tipo_contratacion_encontrada:
            print("No existe el tipo de contratación deseado.")
            return None
        try:
            nueva_contratacion = Contratacion(
                nro_contratacion=nro_contratacion,
                id_contratacion_tipo=tipo_contratacion_encontrada.id,
            )
            nueva_contratacion.save()
            print("Nueva obra registrada con éxito.")
            return nueva_contratacion
        except Exception as e:
            print(f"No se pudo crear la contratación. Error: {e}")
            return None

    except Exception as e:
        print(f"No existe el tipo de contratacion deseado. Error: {e}")
        return None
