@property
def actualizar_porcentaje_avance(self):
    """
    Obtiene el porcentaje de avance de la obra.
    """
    return self._porcentaje_avance

@actualizar_porcentaje_avance.setter
def actualizar_porcentaje_avance(self, nuevo_porcentaje):
    """
    Actualiza el porcentaje de avance de la obra.

    :param nuevo_porcentaje: float, porcentaje a establecer.
    """
    if 0.0 <= nuevo_porcentaje <= 100.0:
        self._porcentaje_avance = nuevo_porcentaje
        self.save()
        print(f"Porcentaje de avance actualizado a {nuevo_porcentaje}%.")
    else:
        raise ValueError("El porcentaje debe estar entre 0 y 100.")

def save(self):
    """
    Simula guardar los datos en la base de datos.
    """
    print("Datos guardados correctamente.")

nuevo_porcentaje = float(input("Ingrese el porcentaje de avance: "))

Obra.actualizar_porcentaje_avance = nuevo_porcentaje