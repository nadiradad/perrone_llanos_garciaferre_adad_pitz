from ObrasConstruccion import *
# ObrasConstruccion.conectar_db()
# ObrasConstruccion.mapear_orm()
# df= ObrasConstruccion.extraer_datos()
# ObrasConstruccion.limpiar_datos(df)
# ObrasConstruccion.cargar_datos(df)
# ObrasConstruccion.obtener_indicadores()
# obra1 =ObrasConstruccion.nueva_obra()
# porcentaje = 20
# obra1.actualizar_porcentaje_avance(porcentaje)
# manoObra=150
# obra1.incrementar_mano_obra(manoObra)
# obra1.finalizar_obra()
# obra2 =ObrasConstruccion.nueva_obra()
# porcentaje1 = 36
# obra2.actualizar_porcentaje_avance(porcentaje1)
# manoObra1=231
# obra2.incrementar_mano_obra(manoObra1)
# obra2.rescindir_obra()

def main():
    print('\n*-------------------------------------------------------------------------------------------------*')
    print('Bienvenido a nuestro Trabajo Practico Final Integrador')
    print('Hecho por: Milagros Llanos, Nadir Adad, Brian Pitz, Pablo Garcia Ferre y Gaston Perrone.')
    print('*-------------------------------------------------------------------------------------------------*\n')
    print('Al ejecutar este archivo lo primero que vamos hacer es configurar la base de datos y cargar los datos del data set...\n')
    ObrasConstruccion.conectar_db()
    ObrasConstruccion.mapear_orm()
    df= ObrasConstruccion.extraer_datos()
    ObrasConstruccion.limpiar_datos(df)
    ObrasConstruccion.cargar_datos(df)
    print('Procesos iniciales finalizados...\n')
    while True:
        print('Opciones: ')
        print('1- Obtener indicadores')
        print('2- Crear Nueva Obra')
        print('3- Actualizar Porcentaje Avance')
        print('4- Incrementar Mano Obra')
        print('5- Finalizar Obra')
        print('6- Rescindir Obra')
        print('7- Salir\n')
        opcion = int(input('ingrese el numero segun la opcion: '))
        match opcion:
            case 1:
                ObrasConstruccion.obtener_indicadores()
            case 2:
                obra1 =ObrasConstruccion.nueva_obra()
            case 3:
                porcentaje = int(input('Ingrese el porcentaje avance: '))
                obra1.actualizar_porcentaje_avance(porcentaje)
            case 4:
                manoObra = int(input('Ingrese la mano obra para incrementar: '))
                obra1.incrementar_mano_obra(manoObra)
            case 5:
                obra1.finalizar_obra()
            case 6:
                obra1.rescindir_obra()
            case 7:
                print('\nSaliendo del TP...')
                print('Gracias vuelva prontos!\n')
                break

if __name__ == "__main__":
    main()