import numpy as np
import pandas as pd
from configs.manager_doc_config import *
from services.leer_excel import leer_excel


############################## DEL 10.1 ########################################

def get_df_datos_documento() -> pd.DataFrame:
    df_datos_documento = leer_excel(ruta_al_excel_para_crear_documento(), nombre_de_hoja=hoja_del_excel_para_crear_documento(), header=None)
    return df_datos_documento

def get_variable_documento(df_datos_documento: pd.DataFrame, nombre_variable: str) -> None | np.ndarray:
    varvalue = None
    for row in df_datos_documento.iterrows():
        if row[1][0] == nombre_variable:
            varvalue = np.array(row[1][1:])
            varvalue = varvalue[~pd.isna(varvalue)]  # Eliminar valores NaN
            return varvalue
    
    if varvalue is None:
        raise ValueError(f"No se encontró la variable '{nombre_variable}' en el DataFrame de datos del documento.")





############################## DEL 10.3 ########################################