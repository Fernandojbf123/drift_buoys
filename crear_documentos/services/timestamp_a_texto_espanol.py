import pandas as pd

def timestamp_a_texto_espanol(fecha: pd.Timestamp, mes_y_anio: bool) -> str:
    meses = {
        1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
        5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto',
        9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
    }
    
    dia = fecha.day
    mes = meses[fecha.month]
    anio = fecha.year
    
    if mes_y_anio:
        return f"{mes} de {anio}"
    
    return f"{dia:02d} de {mes} de {anio}"

