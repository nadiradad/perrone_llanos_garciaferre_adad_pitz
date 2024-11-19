def incrementar_plazo():
    try:
        nuevo_plazo = int(input('Ingrese el nuevo plazo en cantidad de meses: '))
        if nuevo_plazo <= 0:
            print("El plazo debe ser un número positivo.")
            return None
    except ValueError:
        print("Debe ingresar un número entero válido.")
        return None

    nombre_obra = input('Ingrese el nombre de la obra para incrementar el plazo: ')
    try:
        obra = Obra.get_or_none(Obra.nombre == nombre_obra)
        if not obra:
            print("No existe la obra deseada.")
            return None
        
        obra.plazo_meses = nuevo_plazo
        obra.save()
        print(f"El plazo de la obra '{nombre_obra}' ha sido actualizado a {nuevo_plazo} meses.")
    except Exception as e:
        print(f"No se pudo modificar el plazo. Error: {e}")

