def obtener_palabras_singulares_plurales(es_singular: bool) -> dict:
    """
    Retorna un diccionario con palabras en singular o plural según la condición.
    
    Args:
        es_singular: True para singular, False para plural
    
    Returns:
        Diccionario con todas las variantes de palabras
    """
    return {
        # Artículos
        "la_las": "la" if es_singular else "las",
        "el_los": "el" if es_singular else "los",
        "La_Las": "La" if es_singular else "Las",
        "El_Los": "El" if es_singular else "Los",
        "una_unas": "una" if es_singular else "unas",
        "un_unos": "un" if es_singular else "unos",
        
        # Sustantivos
        "campania_campanias": "campaña" if es_singular else "campañas",
        "embarcacion_embarcaciones": "embarcación" if es_singular else "embarcaciones",
        "liberacion_liberaciones": "liberación" if es_singular else "liberaciones",
        
        # Pronombres
        "cual_cuales": "cual" if es_singular else "cuales",
        "este_estos": "este" if es_singular else "estos",
        "esta_estas": "esta" if es_singular else "estas",
        "Este_Estos": "Este" if es_singular else "Estos",
        "Esta_Estas": "Esta" if es_singular else "Estas",
        
        # Verbos
        "fue_fueron": "fue" if es_singular else "fueron",
        "llevo_llevaron": "llevó" if es_singular else "llevaron",
        "dividio_dividieron": "dividió" if es_singular else "dividieron",
    }