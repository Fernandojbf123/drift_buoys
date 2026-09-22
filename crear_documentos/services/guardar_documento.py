import os

def guardar_documento(doc, ruta_a_la_carpeta_de_guardado: str,nombre_archivo:str ="SIN_NOMBRE.docx"):
    """Guarda el documento de Word en la carpeta especificada en la configuración.
    
    Args:
        doc: El documento de Word (objeto Document) a guardar.
        ruta_a_la_carpeta_de_guardado: La ruta a la carpeta donde se guardará el documento.
        nombre_archivo: El nombre del archivo a guardar (por defecto "SIN_NOMBRE.docx").
    
    Returns:
        str: La ruta completa donde se guardó el documento.
    """
    # Obtener la ruta de la carpeta de guardado
    carpeta_guardado = ruta_a_la_carpeta_de_guardado
    
    # Crear la carpeta si no existe
    os.makedirs(carpeta_guardado, exist_ok=True)
    
    # Construir la ruta completa del archivo
    ruta_completa = os.path.join(carpeta_guardado, nombre_archivo)
    
    # Guardar el documento
    doc.save(ruta_completa)
    
    print(f"Documento guardado en: {ruta_completa}")
    
    return ruta_completa
