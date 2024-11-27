from ObrasConstruccion import *
def main():
    print('\n*-------------------------------------------------------------------------------------------------*')
    print('Bienvenido a nuestro Trabajo Practico Final Integrador')
    print('Hecho por: Milagros Llanos, Nadir Adad, Brian Pitz, Pablo Garcia Ferre y Gaston Perrone.')
    print('*-------------------------------------------------------------------------------------------------*\n')
    print('Al ejecutar este archivo lo primero que vamos hacer es configurar la base de datos y cargar los datos del data set...\n')
    ObrasConstruccion.conectar_db()
    ObrasConstruccion.mapear_orm()

    print('Procesos iniciales finalizados...\n')
    while True:
        print('Opciones: ')
        print('1- Importar csv (NECESARIO EJECUTAR ANTES DE LAS OTRAS OPCIONES)')
        print('2- Obtener indicadores')
        print('3- Cumplir consigna Instancia 1')
        print('4- Cumplir consigna Instancia 2')
        print('5- Salir\n')
        opcion = int(input('ingrese el numero segun la opcion: '))
        match opcion:
            case 1:
                df = ObrasConstruccion.extraer_datos()
                df = ObrasConstruccion.limpiar_datos(df)
                ObrasConstruccion.cargar_datos(df)
            case 2:
                ObrasConstruccion.obtener_indicadores()
            case 3:
                obra1 =ObrasConstruccion.nueva_obra()
                porcentaje = 20
                obra1.actualizar_porcentaje_avance(porcentaje)
                manoObra=150
                obra1.incrementar_mano_obra(manoObra)
                obra1.finalizar_obra()
            case 4:
                obra2 =ObrasConstruccion.nueva_obra()
                porcentaje1 = 36
                obra2.actualizar_porcentaje_avance(porcentaje1)
                manoObra1=231
                obra2.incrementar_mano_obra(manoObra1)
                obra2.rescindir_obra()
            case 5:
                print('\nSaliendo del TP...')
                print('Gracias vuelva prontos!\n')
                break

if __name__ == "__main__":
    main()