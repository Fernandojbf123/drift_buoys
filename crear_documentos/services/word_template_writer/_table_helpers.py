"""
Internal helper functions for table manipulation in Word templates.

This module contains low-level functions for filling Word tables with DataFrame data.

Private module - Not intended for direct external use.
Import from the public API in api.py instead.
"""

import pandas as pd
from docx.enum.text import WD_ALIGN_PARAGRAPH


def rellenar_tabla(doc, nombre_marcador, diccionario_de_reemplazos):
    """Rellena una tabla dinámicamente buscando un marcador e insertando datos de un dataframe.
    
    Args:
        doc: El documento de Word (objeto Document).
        nombre_marcador: El nombre del marcador a buscar en la tabla (ej: "<<tabla1>>").
        diccionario_de_reemplazos: Diccionario con los datos a insertar en la tabla.
    
    Descripción:
        La función busca el marcador en todas las tablas del documento.
        Una vez encontrado, guarda el formato de la fila 1 (que contiene el marcador),
        elimina esa fila, y luego inserta todas las filas del dataframe en la tabla
        aplicando el formato guardado.
        
    Ejemplo:
        df = pd.DataFrame({
            'secuencia': [0, 1, 2],
            'localizacion': ['BOT-01', 'BOT-02', 'BOT-03'],
            'lat_plan': [18.5, 18.6, 18.7]
        })
        rellenar_tabla(doc, "<<tabla1>>", df)
        # Resultado: La tabla tendrá 4 filas (1 de encabezado + 3 de datos)
    """
    df = pd.DataFrame(diccionario_de_reemplazos)
    cantidad_de_filas = len(df)
    
    # Buscar la tabla que contiene el marcador
    for table in doc.tables:
        marcador = table.rows[0].cells[0].text
        if nombre_marcador in marcador:
            for idx, row in df.iterrows():
                for icol, col in enumerate(df.columns):  # Agrego los datos del dataframe a la tabla
                    table.rows[idx+1].cells[icol].text = str(row[col])
                    table.rows[idx+1].cells[icol].paragraphs[0].style = doc.styles['texto_tablas_centrado']  # Agregar el estilo daña el alineado vertical y el tamaño de la fila
                    table.rows[idx+1].cells[icol].vertical_alignment = WD_ALIGN_PARAGRAPH.CENTER 
                    table.rows[idx+1].height = 288290
                    
                    if nombre_marcador == "<<tabla2>>" and icol == 1:
                        table.rows[idx+1].cells[icol].paragraphs[0].style = doc.styles['texto_tablas_justificado']  # Agregar el estilo daña el alineado vertical y el tamaño de la fila
                        table.rows[idx+1].cells[icol].vertical_alignment = WD_ALIGN_PARAGRAPH.CENTER
                        table.rows[idx+1].height = 288290  # Ajustar la altura de la fila según sea necesario
                        
                if idx+1 < cantidad_de_filas:  # Agrego una fila vacía para la siguiente iteración (si es que hay más filas por agregar)    
                    table.add_row().cells  # Al terminar agrego una fila vacía para la siguiente iteración (si es que hay más filas por agregar)

            break
        
    return doc
