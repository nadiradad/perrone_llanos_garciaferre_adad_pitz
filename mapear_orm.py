""" 
mapear_orm(), que debe incluir las sentencias necesarias para realizar la creación de la
estructura de la base de datos (tablas y relaciones) utilizando el método de instancia
“create_tables(list)” del módulo “peewee”.
"""

sqlite_db.init('obras_urbanas.db')  # database is now initialized NO SE SI ES NECESARIO
sqlite_db.connect()
try:
    sqlite_db.create_tables([Obra
                            ,Area
                            ,FuenteFinanciamiento
                            ,Comuna
                            ,Etapa
                            ,Licitacion
                            ,TipoContratacion
                            ,Contratacion
                            ,TipoObra
                            ,Relacion])  # no problems.
except peewee.IntegrityError as e:
    print(f'El error de peewee: {e}')
sqlite_db.close()