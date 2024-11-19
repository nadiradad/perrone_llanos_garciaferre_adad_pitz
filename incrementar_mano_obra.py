#Este código iría en modelo_orm.copy()
def incrementar_mano_obra(self):
    incrementar = input("¿Desea incrementar la cantidad de mano de obra? (s/n): ").strip().lower()
    if incrementar == "s":
        cantidad = float(input("Ingrese la cantidad adicional de mano de obra: "))
        self.mano_obra = mano_obra + cantidad
        print(f"Se incrementó la mano de obra en {self.mano_obra}.")