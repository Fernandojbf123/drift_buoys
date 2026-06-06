from pptx import Presentation
import psutil

def abrir_plantilla_esquemas_doris(ruta_a_la_plantilla: str) -> Presentation:
    
   
    for proc in psutil.process_iter():
        if proc.name().lower() == "powerpnt.exe":
            proc.kill()
    """Abre la plantilla PowerPoint del esquema DORIS.

    Descripción:
        Esta función carga la plantilla PowerPoint utilizada para
        generar los esquemas de despliegue de las sondas DORIS.

    Args:
        ruta_a_la_plantilla (str):
            Ruta completa al archivo .pptx.

    Returns:
        Presentation:
            Objeto Presentation de python-pptx con la plantilla cargada.
    """

    try:
        ppt = Presentation(ruta_a_la_plantilla)

    except Exception as e:
        print(f"Error al abrir la plantilla: {e}")
        raise e

    return ppt