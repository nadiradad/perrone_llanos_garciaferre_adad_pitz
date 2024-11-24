def incrementar_mano_obra(self):
    try:
        incrementar = input("¿Desea incrementar la cantidad de mano de obra? (s/n): ").lower() # s = si ; n = no
        if incrementar == "s" # al ser respuesta "s" sigue su ejecución.
            try:
                cantidad = int(input("Ingrese la cantidad adicional de mano de obra: "))
                if cantidad > 0:
                self.mano_obra += cantidad # incrementa la mano de obra
                print(f"Se incrementó la mano de obra en {cantidad}. Total actual: {self.mano_obra}.")
                return self.mano_obra
            except ValueError as e:
                print(f"Error: {e}. Asegúrese de ingresar un número válido y positivo.")
        elif incrementar == "n":
            print("No se realizaron cambios en la cantidad de mano de obra.")
        else:
            print("Opción no válida. Por favor, responda con 's' o 'n'.")
    except Exception as e:
        print(f"Ha ocurrido un error inesperado: {e}")
