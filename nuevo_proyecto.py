
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





   

def adjudicar_obra(self, licitacion_oferta_empresa, expediente_numero):
    try:
        empresa = Empresa.get_or_none(Empresa.licitacion_oferta_empresa == licitacion_oferta_empresa)
        
        if empresa:
            relacion = Relacion.get_or_none(Relacion.id_licitaciones == empresa.id, Relacion.id_obras == self.id)
            
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
