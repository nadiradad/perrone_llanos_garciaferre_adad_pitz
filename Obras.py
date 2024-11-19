from gestionar_obras import *
from modelo_orm import *

class Obra:
    def nuevo_proyecto(self, nombre, descripcion, expediente_numero, fecha_inicio, plazo_meses):
           try:
               self.nombre = nombre
               self.descripcion = descripcion
               self.expediente_numero = expediente_numero
               self.fecha_inicio = fecha_inicio
               self.plazo_meses = plazo_meses
               self.save()  
               print(f"Proyecto '{self.nombre}' registrado como nuevo proyecto.")
           except Exception as e:
               print(f"Error: {e}")

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
    def adjudicar_obra(self, licitacion_oferta_empresa, expediente_numero):
        try:
            empresa = Empresa.get_or_none(Empresa.licitacion_oferta_empresa == licitacion_oferta_empresa)

            if empresa:
                relacion = Relacion.get_or_none(Relacion.id_empresas == empresa.id, Relacion.id_obras == self.id)

                if relacion:
                    self.licitacion_oferta_empresa = licitacion_oferta_empresa
                    self.expediente_numero = expediente_numero
                    self.save()
                    print(f"Obra {self.nombre} adjudicada exitosamente con la licitación {licitacion_oferta_empresa}.")
                else:
                    print(f"No existe una relación válida entre la obra {self.nombre} y la empresa.")
            else:
                print(f"La empresa con la licitación {licitacion_oferta_empresa} no existe.")

        except Exception as e:
            print(f"Error: {e}")
        
    def iniciar_obra():
        pass

    def actualizar_porcentaje_avance():
        pass

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

    def incrementar_mano_obra():
        pass

    def finalizar_obra(self):
        try:
            Id = int(input('Ingrese el Id de la obra a finalizar: '))

            query = (Etapa.update(etapa='Finalizada', porcentaje_avance=100)
                     .where(Obra.id == Id)
                     .join(Relacion, on=(Etapa.id == Relacion.id_etapas))
                     .join(Obra, on=(Relacion.id_obra == Obra.id)))  

            rows_updated = query.execute()

            if rows_updated == 0:
                mensaje = f"No se encontró una obra con el ID {Id}."
                print(mensaje)
                return False
            else:
                mensaje = f"La obra con ID {Id} ha sido finalizada correctamente."
                print(mensaje)
                return True  

        except ValueError:
            mensaje = "El ID ingresado no es válido. Por favor, ingrese un número entero."
            print(mensaje)
            return False  
        except Exception as e:
            mensaje = f"Se produjo un error al intentar finalizar la obra: {e}"
            print(mensaje)
            return False
    
    def rescindir_obra():
        pass


