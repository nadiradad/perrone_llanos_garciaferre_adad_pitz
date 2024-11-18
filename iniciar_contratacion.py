def iniciar_contratacion(self, contratacion_tipo, nro_contratacion):
        nro_contratacion = input('Ingrese el numero de contratacion: ')
        contratacion_tipo = input('Ingrese el tipo de contratacion: ')
        contratacion_tipo, created = TipoContratacion.get_or_create(contratacion_tipo=contratacion_tipo)
        nueva_contratacion = Contratacion(
                nro_contratacion=nro_contratacion,
                contratacion_tipo=contratacion_tipo,
            )
        nueva_contratacion.save()
        print("Nueva obra registrada con éxito.")
        return nueva_obra