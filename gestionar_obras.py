import pandas as pd
from peewee import *
from modelo_orm import *
from abc import ABC, abstractmethod
class GestionarObra(ABC):
    def __init__(self):
        super().__init__()
    
    @classmethod
    @abstractmethod
    def limpiar_datos(cls, df: pd.DataFrame) -> pd.DataFrame:
       pass

    @classmethod
    @abstractmethod
    def extraer_datos():
       pass

    @classmethod
    @abstractmethod
    def conectar_db():
       pass

    @classmethod
    @abstractmethod
    def mapear_orm():
       pass

    @classmethod
    @abstractmethod
    def cargar_datos(df):
       pass

    @classmethod
    @abstractmethod
    def nueva_obra():
       pass

    @classmethod
    @abstractmethod
    def obtener_listado_areas_responsables():
       pass

    @classmethod
    @abstractmethod
    def obtener_listado_tipos_obra():
       pass

    @classmethod
    @abstractmethod
    def obtener_cantidad_obras_por_etapa():
       pass
    
    @classmethod
    @abstractmethod
    def obtener_cantidad_obras_monto_por_obra():
        pass
    
    @classmethod
    @abstractmethod
    def obtener_barrios_por_comuna():
        pass
    
    @classmethod
    @abstractmethod
    def obtener_cantidad_obras_finalizadas_monto_total_comuna1():
        pass

    @classmethod
    @abstractmethod
    def obtener_cantidad_obras_finalizadas_menos_24_meses():
        pass
    
    @classmethod
    @abstractmethod    
    def obtener_porcentaje_obras_finalizadas(): 
        pass
        
    @classmethod
    @abstractmethod    
    def obtener_cantidad_total_mano_obra():
        pass

    @classmethod
    @abstractmethod  
    def obtener_monto_total_inversion():
        pass

    @classmethod
    @abstractmethod  
    def obtener_indicadores():
       pass