import matplotlib.dates as mdates
import locale

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # Unix/macOS

# Diccionario para pasar de algo con punto a sin punto
meses_sin_punto = {
    'ene.': 'Ene', 'feb.': 'Feb', 'mar.': 'Mar', 'abr.': 'Abr',
    'may.': 'May', 'jun.': 'Jun', 'jul.': 'Jul', 'ago.': 'Ago',
    'sep.': 'Sep', 'oct.': 'Oct', 'nov.': 'Nov', 'dic.': 'Dic'
}

def GraFormatoFecha(x, pos):
    """
    Descripción:
        Coloca el formato de la fecha en el eje X como dia/mes/año.
        Formatea fechas numéricas (en formato de Matplotlib) a una cadena legible en español
        con el formato 'dd/Mes/yyyy'
        Utiliza abreviaturas de meses sin punto (e.g., 'Ene' en lugar de 'ene.')

    Parámetros:
        x (float): Valor de fecha en formato numérico (Matplotlib date).
        pos (int): Posición del tick (requerido por Matplotlib pero no se usa en esta función).

    Retorna:
       str: Cadena con la fecha formateada, por ejemplo: '03/Feb/2025'
       
    Ejemplo:    
        GraFormatoFecha(738885.0, 0)
        '03/Feb/2025'
        
    Funciones auxiliares: 
        Ninguna
    
    Categoría:
        Gráficos
    
    """
    
    fecha = mdates.num2date(x)
    mes = fecha.strftime('%b').lower() 
    mes_limpio = meses_sin_punto.get(mes, mes)
    return f"{fecha.day:02}/{mes_limpio}/{fecha.year}"

