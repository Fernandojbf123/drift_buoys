import os
from docx import Document

from crear_documentos.configs.manager_doc_config import get_nombre_de_la_plantilla_de_word


def abrir_plantilla_doris() -> Document:
    """Abre el documento plantilla de DORIS y devuelve un objeto Document.

    Descripción:
        Esta función carga el documento plantilla de Word ubicado en la carpeta
        de plantillas para ser utilizado en la generación de documentos de
        despliegue de sondas DORIS.

    Retorna:
        Document: Un objeto Document de python-docx con la plantilla cargada."""
    
    # Construir la ruta al archivo plantilla
    ruta_base = os.path.dirname(os.path.dirname(__file__))
    ruta_plantilla = os.path.join(ruta_base, "utils", "plantillas", get_nombre_de_la_plantilla_de_word())
    
    # Abrir y retornar el documento
    try:
        documento = Document(ruta_plantilla)    
    except Exception as e:
        print(f"Error al abrir la plantilla: {e}")
        raise e
    
    return documento
