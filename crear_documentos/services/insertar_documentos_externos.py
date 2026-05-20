from docx import Document
from copy import deepcopy

def insertar_documentos_externos(paragraph, key, lista_rutas_documentos):
    """Inserta el contenido de uno o varios documentos Word externos.
    
    Args:
        paragraph: El párrafo donde está el marcador.
        key: El marcador a buscar.
        lista_rutas_documentos: Lista de rutas a documentos Word o una sola ruta (string).
    
    Returns:
        True si se insertaron los documentos, False si no se encontró el marcador.
    """
    full_text = "".join(run.text for run in paragraph.runs)
    
    if key not in full_text:
        return False
    
    # Convertir a lista si es un solo string
    if isinstance(lista_rutas_documentos, str):
        lista_rutas_documentos = [lista_rutas_documentos]
    
    # Limpiar el párrafo marcador
    for run in paragraph.runs:
        run.text = ""
    
    # Obtener referencias
    p_element = paragraph._element
    parent = p_element.getparent()
    indice_insercion = parent.index(p_element)
    offset = 0
    
    # Insertar cada documento
    for ruta_doc in lista_rutas_documentos:
        if not exists(ruta_doc):
            # Agregar mensaje de error como párrafo
            p_error = OxmlElement('w:p')
            run = OxmlElement('w:r')
            text = OxmlElement('w:t')
            text.text = f"[Error: No se encontró {ruta_doc}]"
            run.append(text)
            p_error.append(run)
            parent.insert(indice_insercion + offset + 1, p_error)
            offset += 1
            continue
        
        # Cargar documento externo
        doc_externo = Document(ruta_doc)
        
        # Copiar todos los elementos
        for elemento in doc_externo.element.body:
            elemento_copiado = deepcopy(elemento)
            parent.insert(indice_insercion + offset + 1, elemento_copiado)
            offset += 1
        
        # Agregar salto de página entre documentos (opcional)
        if lista_rutas_documentos.index(ruta_doc) < len(lista_rutas_documentos) - 1:
            # Agregar salto de página
            p_break = OxmlElement('w:p')
            pPr = OxmlElement('w:pPr')
            pageBreak = OxmlElement('w:pageBreakBefore')
            pPr.append(pageBreak)
            p_break.append(pPr)
            parent.insert(indice_insercion + offset + 1, p_break)
            offset += 1
    
    # Eliminar el párrafo marcador original
    parent.remove(p_element)
    
    return True