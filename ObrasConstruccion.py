from gestionar_obras import *

class ObrasConstruccion(GestionarObra):
    
    @classmethod
    def limpiar_datos(cls, df: pd.DataFrame) -> pd.DataFrame:
        df = df.dropna(how='all')  
        df = df.fillna({col: 'Desconocido' if df[col].dtype == 'object' else 0 
            for col in df.columns})
        return df