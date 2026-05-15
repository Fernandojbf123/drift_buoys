import os
from docx import Document

def abrir_plantilla_doris(ruta_a_la_plantilla: str) -> Document:
    """Abre el documento plantilla de DORIS y devuelve un objeto Document.

    Descripción:
        Esta función carga el documento plantilla de Word ubicado en la carpeta
        de plantillas para ser utilizado en la generación de documentos de
        despliegue de sondas DORIS.

    Retorna:
        Document: Un objeto Document de python-docx con la plantilla cargada."""
    
    # Abrir y retornar el documento
    try:
        documento = Document(ruta_a_la_plantilla)    
    except Exception as e:
        print(f"Error al abrir la plantilla: {e}")
        raise e
    
    return documento
