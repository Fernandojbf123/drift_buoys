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

puertos = {
    "El Bellote": {"lon": -93.133841, "lat": 18.429949},
    "Dos Bocas": {"lon": -93.1938, "lat": 18.4341667},
    "Cd Carmen": {"lon": -91.839, "lat": 18.655},
    "Sanchez Magallanes": {"lon": -93.853048, "lat": 18.299602},
    "Coatzacoalcos": {"lon": -94.41, "lat": 18.14},
    "Tecolutla": {"lon": -97.006, "lat": 20.474},
    "Tuxpan": {"lon": -97.306757, "lat": 20.966327},
    "Isla Aguada": {"lon": -91.507021, "lat": 18.819539},
    "Pto_Veracruz": {"lon": -96.123816, "lat": 19.192781},
    "Altamira": {"lon": -97.855436, "lat": 22.490824},
    "Tampico": {"lon": -97.788611, "lat": 22.262412},
    "La Pesca": {"lon": -97.776662, "lat": 23.787006},
    "Alvarado": {"lon": -95.76181, "lat": 18.77143},
    "El Mezquital": {"lon": -97.443055, "lat": 25.243333}
}