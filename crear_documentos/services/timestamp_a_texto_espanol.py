import pandas as pd

def timestamp_a_texto_espanol(fecha: pd.Timestamp) -> str:
    meses = {
        1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
        5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto',
        9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
    }
    
    dia = fecha.day
    mes = meses[fecha.month]
    anio = fecha.year
    
    return f"{dia:02d} de {mes} de {anio}"

# Uso:
fecha = pd.Timestamp('2026-01-15')
resultado = timestamp_a_texto_espanol(fecha)
# Resultado: "15 de enero de 2026"