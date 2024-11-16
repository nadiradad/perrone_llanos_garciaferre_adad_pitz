import pandas as pd

def importar_datos_csv():

    archivo_csv = "/observatorio-de-obras-urbanas.csv"

    try:
        df = pd.read_csv(archivo_csv, sep=",")
        return df
    except FileNotFoundError as e:
        print("Error al conectar con el dataset.", e)
        return False