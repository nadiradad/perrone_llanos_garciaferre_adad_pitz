def incrementar_plazo():
    nuevo_plazo = input('Ingrese el nuevo plazo en cantidad de meses: ')
    nombre_obra = input('Ingrese el nombre de la obra para incrementar el plazo: ')
    try:
        obra = Obra.get(Obra.nombre == nombre_obra)
        obra.plazo_meses = nuevo_plazo      # Asigna el nuevo valor a plazo_meses
        obra.save()                         # Guarda los cambios en la base de datos
        print(f"El plazo de la obra {nombre_obra} ha sido actualizado a {nuevo_plazo} meses.")
    except Obra.DoesNotExist:
        print("No se encontró la obra con ese nombre.")
