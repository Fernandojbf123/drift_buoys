import os
from crear_documentos.configs.manager_doc_config import get_ruta_a_carpeta_de_guardado_del_documento


def guardar_documento(doc, nombre_archivo="ASM-CICESE-10.1.docx"):
    """Guarda el documento de Word en la carpeta especificada en la configuración.
    
    Args:
        doc: El documento de Word (objeto Document) a guardar.
        nombre_archivo: El nombre del archivo a guardar (por defecto "ASM-CICESE-10.1.docx").
    
    Returns:
        str: La ruta completa donde se guardó el documento.
    """
    # Obtener la ruta de la carpeta de guardado
    carpeta_guardado = get_ruta_a_carpeta_de_guardado_del_documento()
    
    # Crear la carpeta si no existe
    os.makedirs(carpeta_guardado, exist_ok=True)
    
    # Construir la ruta completa del archivo
    ruta_completa = os.path.join(carpeta_guardado, nombre_archivo)
    
    # Guardar el documento
    doc.save(ruta_completa)
    
    print(f"Documento guardado en: {ruta_completa}")
    
    return ruta_completa
