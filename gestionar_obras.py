from abc import ABC
import pandas as pd #Importamos PANDAS para importar el dataset de "observatorio-de-obras-urbanas.csv"
import numpy as np #Importamos NUMPY para la manipulaciòn del dataset.

class GestionarObra(ABC):
    def __init__(self):
        super().__init__()

    def extraer_datos():
        """que debe incluir las sentencias necesarias para manipular el dataset a
través de un objeto Dataframe del módulo “pandas”."""
        pass

    def conectar_db():
        """que debe incluir las sentencias necesarias para realizar la conexión a la base de datos “obras_urbanas.db”."""
        pass

    def mapear_orm():
        """que debe incluir las sentencias necesarias para realizar la creación de la estructura de la base de datos (tablas y relaciones) utilizando el método de instancia “create_tables(list)” del módulo “peewee” """
        pass

    def limpiar_datos():
        """que debe incluir las sentencias necesarias para realizar la “limpieza” de los datos nulos y no accesibles del Dataframe."""
        pass

    def cargar_datos():
        """que debe incluir las sentencias necesarias para persistir los datos de las obras (ya transformados y “limpios”) que contiene el objeto Dataframe en la base de datos relacional SQLite. Para ello se debe utilizar el método de clase Model create() en cada una de las clase del modelo ORM definido."""
        pass

    def nueva_obra():
        """que debe incluir las sentencias necesarias para crear nuevas instancias de Obra. Se deben considerar los siguientes requisitos:
        • Todos los valores requeridos para la creación de estas nuevas instancias deben ser ingresados por teclado.
        • Para los valores correspondientes a registros de tablas relacionadas (foreign key), el valor ingresado debe buscarse en la tabla correspondiente mediante sentencia de búsqueda ORM, para obtener la instancia relacionada, si el valor ingresado no existe en la tabla, se le debe informar al usuario y solicitarle un nuevo ingreso por teclado.
        • Para persistir en la BD los datos de la nueva instancia de Obra debe usarse el método save() de Model del módulo “peewee”. 
        • Este método debe retornar la nueva instancia de obra."""
        pass

    def obtener_indicadores():
        """que debe incluir las sentencias necesarias para obtener información de las obras existentes en la base de datos SQLite a través de sentencias ORM."""
        pass