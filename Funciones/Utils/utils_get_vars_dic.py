from Configs.diccionario_variables import ylabels, var_names
# Funciones asociadas al diccionario de variables

def obtener_nombres_estandarizados(nombres_de_columnas_crudas: list) -> list:
    """
    Cambia los nombres de las columnas de un DataFrame a nombres estandarizados
    según el diccionario var_names definido en Configs/diccionario_variables.py.
    
    Parámetros:
    nombres_de_columnas_crudas (list): Lista de nombres de columnas originales.
    
    Retorna:
    list: Lista de nombres de columnas estandarizados.
    """
    nombres_estandarizados = []
    
    for nombre in nombres_de_columnas_crudas:
        nombre_encontrado = False
        for estandarizado, variantes in var_names.items():
            if nombre in variantes:
                nombres_estandarizados.append(estandarizado)
                nombre_encontrado = True
                break
        if not nombre_encontrado:
            nombres_estandarizados.append(nombre)  # Mantener el nombre original si no se encuentra
            print(f"Advertencia: La variable '{nombre}' no tiene un nombre estandarizado definido. Agregalo al archivo Configs/diccionario_variables.py.")
    return nombres_estandarizados

def get_ylabels(var_names):
    return [ylabels[var] for var in var_names]