"""
Internal helper functions for text manipulation in Word templates.

This module contains low-level functions for replacing text variables in paragraphs.

Private module - Not intended for direct external use.
Import from the public API in api.py instead.
"""


def replace_text_variables_in_paragraph(paragraph, lista_variables):
    """Reemplaza múltiples marcadores de posición en un párrafo de Word de una sola vez.
    
    Args:
        paragraph: El párrafo donde buscar los marcadores.
        lista_variables: Lista de tuplas (key, value) con los marcadores y sus valores.
                        Ejemplo: [("<<orden_de_servicio>>", "202"), ("<<numero_de_sondas>>", 5)]
    
    Esta función reemplaza todas las variables en un solo paso, evitando problemas
    de estado cuando hay múltiples variables en el mismo párrafo.
    """
    # Obtener el texto completo del párrafo
    full_text = "".join(run.text for run in paragraph.runs)
    
    # Reemplazar todas las variables en el texto completo
    texto_reemplazado = full_text
    for key, value in lista_variables:
        if key in texto_reemplazado:
            # Convertir value a string
            new_value = str(value[0]) if isinstance(value, list) else str(value)
            # Reemplazar todas las ocurrencias de esta variable
            texto_reemplazado = texto_reemplazado.replace(key, new_value)
    
    # Si no hubo cambios, retornar
    if texto_reemplazado == full_text:
        return paragraph
    
    # Limpiar todos los runs excepto el primero
    primer_run = paragraph.runs[0] if paragraph.runs else paragraph.add_run()
    primer_run.text = texto_reemplazado
    
    # Limpiar el resto de runs
    for i in range(1, len(paragraph.runs)):
        paragraph.runs[i].text = ""
    
    return paragraph
