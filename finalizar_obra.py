class Obra(BaseModel):
    id = AutoField(primary_key=True)
    nombre = CharField()
    descripcion = TextField()
    expediente_numero = CharField()
    mano_obra = IntegerField()
    destacada = CharField(max_length=2)
    fecha_inicio = DateField()
    fecha_fin_inicial = DateField()
    plazo_meses = IntegerField()

    etapa = ForeignKeyField(Etapa, backref='obras') # relación con la clase Etapa

    def __str__(self):
        return self.nombre #cuando se imprima una instancia de Obra, se va a mostrar su nombre

    class Meta:
        db_table = 'Obras' #esta configuración indica que la tabla en la base de datos para la clase Obra se llamará Obras

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
    

    





