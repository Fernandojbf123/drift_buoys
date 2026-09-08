"""
Internal helper functions for text manipulation in Word templates.

This module contains low-level functions for replacing text variables in paragraphs.

Private module - Not intended for direct external use.
Import from the public API in api.py instead.
"""

from copy import deepcopy
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def insertar_referencia_en_marcador(doc, marcador, bookmark, incluir_corchetes=True):
    """Reemplaza un marcador por un campo REF en su posición original."""
    for parrafo in doc.paragraphs:
        runs = parrafo.runs
        texto_completo = "".join(run.text or "" for run in runs)
        inicio = texto_completo.find(marcador)
        if inicio == -1:
            continue

        fin = inicio + len(marcador)
        posiciones = []
        offset = 0

        for indice, run in enumerate(runs):
            texto_run = run.text or ""
            siguiente_offset = offset + len(texto_run)
            if siguiente_offset > inicio and offset < fin:
                posiciones.append((indice, offset, siguiente_offset))
            offset = siguiente_offset

        primer_indice, primer_offset, _ = posiciones[0]
        ultimo_indice, _, ultimo_fin = posiciones[-1]
        primer_run = runs[primer_indice]
        ultimo_run = runs[ultimo_indice]
        formato_referencia = deepcopy(ultimo_run._r.rPr)

        texto_antes = (primer_run.text or "")[:inicio - primer_offset]
        inicio_ultimo = ultimo_fin - len(ultimo_run.text or "")
        texto_despues = (ultimo_run.text or "")[fin - inicio_ultimo:]

        if primer_indice == ultimo_indice:
            primer_run.text = texto_antes + texto_despues
        else:
            primer_run.text = texto_antes
            for indice, _, _ in posiciones[1:-1]:
                runs[indice].text = ""
            ultimo_run.text = texto_despues

        formato = formato_referencia
        texto_referencia = f"[{1}]" if incluir_corchetes else "1"
        elementos_referencia = [
            _crear_enlace_interno(bookmark, texto_referencia, formato)
        ]

        # El origen debe aparecer al final del párrafo, aunque el marcador
        # esté escrito al inicio de la plantilla.
        runs_con_texto = [run for run in parrafo.runs if run.text]
        run_final = runs_con_texto[-1] if runs_con_texto else primer_run
        texto_final = run_final.text or ""
        puntuacion_final = texto_final[-1:] if texto_final else ""
        puntuacion = ".,;:!?)]}"

        if puntuacion_final in puntuacion:
            run_final.text = texto_final[:-1]
            run_puntuacion = _crear_run_texto(puntuacion_final, run_final._r.rPr)
            ancla = run_final._r
        else:
            run_puntuacion = None
            ancla = run_final._r

        for elemento in elementos_referencia:
            ancla.addnext(elemento)
            ancla = elemento

        if run_puntuacion is not None:
            ancla.addnext(run_puntuacion)

        return True

    print(f"ADVERTENCIA: no se encontró '{marcador}' en la plantilla.")
    return False


def insertar_destino_en_marcador(doc, marcador, bookmark, numero="1"):
    """Reemplaza un marcador por [numero] y crea el bookmark de destino."""
    for parrafo in doc.paragraphs:
        for run in parrafo.runs:
            if marcador not in (run.text or ""):
                continue

            texto = run.text or ""
            antes, despues = texto.split(marcador, 1)
            formato = deepcopy(run._r.rPr) if run._r.rPr is not None else None
            run.text = antes

            elementos = []
            if antes:
                pass

            elementos.append(_crear_run_texto("[", formato))

            inicio = OxmlElement("w:bookmarkStart")
            inicio.set(qn("w:id"), "2001")
            inicio.set(qn("w:name"), bookmark)
            elementos.append(inicio)
            elementos.append(_crear_run_texto(numero, formato))

            fin = OxmlElement("w:bookmarkEnd")
            fin.set(qn("w:id"), "2001")
            elementos.append(fin)
            elementos.append(_crear_run_texto("]", formato))

            ancla = run._r
            for elemento in elementos:
                ancla.addnext(elemento)
                ancla = elemento

            if despues:
                run_despues = _crear_run_texto(despues, formato)
                ancla.addnext(run_despues)

            return True

    print(f"ADVERTENCIA: no se encontró '{marcador}' en la plantilla.")
    return False


def _crear_run_texto(texto, formato=None):
    run = OxmlElement("w:r")
    if formato is not None:
        run.append(deepcopy(formato))
    run.append(_crear_texto(texto))
    return run


def _crear_enlace_interno(bookmark, texto, formato=None):
    enlace = OxmlElement("w:hyperlink")
    enlace.set(qn("w:anchor"), bookmark)
    enlace.set(qn("w:history"), "1")
    enlace.append(_crear_run_texto(texto, formato))
    return enlace


def _crear_texto(texto):
    nodo_texto = OxmlElement("w:t")
    nodo_texto.text = texto
    return nodo_texto


def _crear_campo_ref(bookmark, formato=None):
    run_inicio = OxmlElement("w:r")
    run_instruccion = OxmlElement("w:r")
    run_separador = OxmlElement("w:r")
    run_resultado = OxmlElement("w:r")
    run_fin = OxmlElement("w:r")

    for run in (run_inicio, run_instruccion, run_separador, run_resultado, run_fin):
        if formato is not None:
            run.append(deepcopy(formato))

    inicio = OxmlElement("w:fldChar")
    inicio.set(qn("w:fldCharType"), "begin")
    run_inicio.append(inicio)

    instruccion = OxmlElement("w:instrText")
    instruccion.set(qn("xml:space"), "preserve")
    instruccion.text = f" REF {bookmark} \\h "
    run_instruccion.append(instruccion)

    separador = OxmlElement("w:fldChar")
    separador.set(qn("w:fldCharType"), "separate")
    run_separador.append(separador)

    run_resultado.append(_crear_texto("1"))

    fin = OxmlElement("w:fldChar")
    fin.set(qn("w:fldCharType"), "end")
    run_fin.append(fin)

    return [run_inicio, run_instruccion, run_separador, run_resultado, run_fin]


def replace_text_variables_in_paragraph(paragraph, lista_variables):
    """Reemplaza múltiples marcadores de posición en un párrafo de Word de una sola vez.
    
    Args:
        paragraph: El párrafo donde buscar los marcadores.
        lista_variables: Lista de tuplas (key, value) con los marcadores y sus valores.
                        Ejemplo: [("<<orden_de_servicio>>", "202"), ("<<numero_de_sondas>>", 5)]
    
    Esta función reemplaza todas las variables en un solo paso, evitando problemas
    de estado cuando hay múltiples variables en el mismo párrafo.
    """
    # Reemplazar cada marcador dentro de sus runs originales. Así se conserva
    # el formato de todo el texto que no pertenece al marcador.
    for key, value in lista_variables:
        new_value = str(value[0]) if isinstance(value, list) else str(value)
        while True:
            runs = paragraph.runs
            texto_completo = "".join(run.text or "" for run in runs)
            inicio = texto_completo.find(key)
            if inicio == -1:
                break

            fin = inicio + len(key)
            posiciones = []
            offset = 0

            for indice, run in enumerate(runs):
                texto_run = run.text or ""
                siguiente_offset = offset + len(texto_run)
                if siguiente_offset > inicio and offset < fin:
                    posiciones.append((indice, offset, siguiente_offset))
                offset = siguiente_offset

            primer_indice, primer_offset, _ = posiciones[0]
            ultimo_indice, _, ultimo_fin = posiciones[-1]
            primer_run = runs[primer_indice]
            ultimo_run = runs[ultimo_indice]

            prefijo = (primer_run.text or "")[:inicio - primer_offset]
            sufijo = (ultimo_run.text or "")[fin - (ultimo_fin - len(ultimo_run.text or "")):]

            if primer_indice == ultimo_indice:
                primer_run.text = prefijo + new_value + sufijo
            else:
                primer_run.text = prefijo + new_value
                for indice, _, _ in posiciones[1:-1]:
                    runs[indice].text = ""
                ultimo_run.text = sufijo
    
    return paragraph

def replace_text_variables_in_tables(doc, diccionario_de_reemplazos):
    """Reemplaza marcadores de posición en todas las celdas de todas las tablas del documento.
    
    Args:
        doc: Objeto Document de python-docx
        diccionario_de_reemplazos: Dict con {<<variable>>: valor}
    
    Comportamiento:
        - Itera todas las tablas del documento
        - Busca en todos los párrafos de cada celda
        - Ignora marcadores que inician con: <<fig_, <<ref_, <<tabla_, <<external_doc
        - Reutiliza replace_text_variables_in_paragraph() para preservar formato
    
    Caso de uso típico:
        Tablas semi-estáticas con textos fijos + variables individuales.
        
        Ejemplo en plantilla Word:
        ┌──────────────────────────────┬─────────────────────┐
        │        <<nombre_equipo>>                           │ ← Encabezado
        ├──────────────────────────────┼─────────────────────┤
        │ Serial                       │ <<serial>>          │ ← Fijos + variables
        │ Profundidad máxima           │ <<profundidad>>     │
        └──────────────────────────────┴─────────────────────┘
    
    Nota:
        Complementa a reemplazar_texto_en_plantilla() que solo busca en doc.paragraphs.
        Para tablas dinámicas (llenar con DataFrame completo), usar rellenar_tablas_en_plantilla().
    """
    # Filtrar variables de texto (ignorar fig, ref, tabla, external_doc)
    # Verificar que INICIE con estos prefijos, no solo que los contenga
    prefijos_excluidos = ["<<fig_", "<<ref_", "<<tabla_", "<<external_doc"]
    variables_texto = {
        k: v for k, v in diccionario_de_reemplazos.items() 
        if not any(k.startswith(prefix) for prefix in prefijos_excluidos)
    }
    
    # Iterar todas las tablas del documento
    for table in doc.tables:
        # Iterar todas las celdas de la tabla
        for row in table.rows:
            for cell in row.cells:
                # Cada celda puede tener múltiples párrafos
                for parrafo in cell.paragraphs:
                    # Encontrar variables en este párrafo
                    variables_en_parrafo = []
                    for variable, dato in variables_texto.items():
                        if variable in parrafo.text:
                            variables_en_parrafo.append((variable, dato))
                    
                    # Si hay variables, reemplazarlas (reutiliza función existente)
                    if variables_en_parrafo:
                        replace_text_variables_in_paragraph(parrafo, variables_en_parrafo)
    
    msg = "Se reemplazaron las variables en las tablas del documento."
    print(msg)
