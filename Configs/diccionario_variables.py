# Este diccionario registra todos los posibles nombres con los que puede aparecer cada variable en los archivos de datos crudos.
# Se utiliza para estandarizar los nombres de las variables al procesar los datos.
# El key es el nombre estandarizado que se usará en el análisis y los valores son listas de posibles nombres alternativos.
# Los values incluyen variaciones en mayúsculas/minúsculas y sinónimos comunes de cómo se pueden nombrar las variables en las tablas de datos crudos.
var_names = {
    "tspan_de_envio": ["fecha","estampa_de_tiempo","time", "Time", "tspan", "Tspan", "tspan_de_envio", "Time_send"],
    "latitud": ["lat", "Lat", "LAT", "latitud", "Latitude", "latitude"],
    "longitud": ["lon", "Lon", "LON", "logitud", "longitud", "Longitude", "longitude"],
    "distancia": ["distance", "Distance", "distancia","Distancia"],
    "temperatura_mar": ["temp","Temp", "Temperatura", "Temperature", "temperatura_mar", "temperature_sea"],
    "rap_corriente": ["speed","Rapidez", "rapidez", "Rap", "rap_corriente"],  
    "dir_corriente": ["direction", "Direction", "Dir", "dir_corriente"],
    "dir_corriente_texto": ["direction_gen", "Direction_gen", "Dir_gen", "dir_corriente_texto"],
    "u_corriente": ["U", "u", "Velocidad_U", "velocidad_u", "u_corriente", "velocity_u"],
    "v_corriente": ["V", "v", "Velocidad_V", "velocidad_v", "v_corriente", "velocity_v"],
    "voltaje": ["volt", "Voltage", "voltage"]
}

# Este diccionario proporciona etiquetas legibles para cada variable, que se utilizan en los gráficos y reportes.
# El key es el nombre estandarizado de la variable y debe coincidir con el key de la variable var_names
# El value es la etiqueta con unidades.
ylabels = {
    "temperatura_mar": "Temp (°C)",
    "rap_corriente": "Rap (m/s)",
    "dir_corriente": "Dir (°)",
    "u_corriente": "u (m/s)",
    "v_corriente": "v (m/s)",
    "voltaje": "Volt (V)"
}