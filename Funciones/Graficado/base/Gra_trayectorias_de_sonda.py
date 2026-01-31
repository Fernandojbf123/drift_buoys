import pandas as pd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

def graficar_trayectorias_de_sonda(df_excel_de_despliegue: pd.DataFrame, 
                                   serial: str,
                                   df_datos_de_la_sonda: pd.DataFrame = None,
                                   df_datos_previos_de_la_sonda: pd.DataFrame = None,
                                   graficar_trayectorias_pasadas: bool = True) -> plt.PathCollection:
    """
    Descripción:
        Grafica la trayectoria completa de una boya derivadora (drift buoy) sobre un mapa,
        mostrando la posición inicial, final y el recorrido coloreado por la rapidez de corriente.
        La función utiliza proyección Cartopy y requiere un axis con proyección PlateCarree activo.

    Parámetros:
        df_excel_de_despliegue (pd.DataFrame): DataFrame con información de despliegue de sondas.
            Debe contener las columnas:
            - 'serie_de_sonda' (str): Número de serie de la sonda.
            - 'latitud_de_despliegue' (float): Latitud inicial del despliegue (grados).
            - 'longitud_de_despliegue' (float): Longitud inicial del despliegue (grados, valor positivo).
        serial (str): Número de serie de la sonda específica a graficar.
        df_datos_de_la_sonda (pd.DataFrame): DataFrame con los datos temporales de la sonda.
            Debe contener las columnas:
            - 'latitud' (float): Serie temporal de latitudes (grados).
            - 'longitud' (float): Serie temporal de longitudes (grados, negativos para oeste).
            - 'rap_corriente' (float): Rapidez de corriente en cada posición (m/s).

    Retorna:
        matplotlib.collections.PathCollection: Objeto mapeable del scatter de la trayectoria,
            útil para agregar un colorbar posteriormente.

    Ejemplo:
        >>> import matplotlib.pyplot as plt
        >>> import cartopy.crs as ccrs
        >>> import pandas as pd
        >>> # Datos de despliegue
        >>> df_despliegue = pd.DataFrame({
        ...     'serie_de_sonda': ['300534063808640', '300534063808641'],
        ...     'latitud_de_despliegue': [20.5, 21.0],
        ...     'longitud_de_despliegue': [95.0, 96.0]
        ... })
        >>> # Datos de trayectoria
        >>> df_trayectoria = pd.DataFrame({
        ...     'latitud': [20.5, 20.6, 20.7, 20.8],
        ...     'longitud': [-95.0, -95.1, -95.2, -95.3],
        ...     'rap_corriente': [0.3, 0.5, 0.8, 1.2]
        ... })
        >>> # Crear mapa y graficar
        >>> fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
        >>> ax.coastlines()
        >>> obj_scatter = graficar_trayectorias_de_sonda(df_despliegue, '300534063808640', df_trayectoria)
        >>> plt.colorbar(obj_scatter, label='Rapidez corriente (m/s)')
        >>> plt.show()

    Notas:
        - El punto inicial se marca en amarillo con borde negro (tamaño 50).
        - El punto final se marca en rojo con borde negro (tamaño 50).
        - La trayectoria se colorea según rapidez de corriente usando colormap 'jet'.
        - Rango de colormap: 0 a 1.5 m/s.
        - La longitud de despliegue se convierte a negativa (convención oeste).
        - Requiere un axis con proyección Cartopy activo (se usa plt.scatter directamente).

    Funciones auxiliares:
        Ninguna

    Categoría:
        Gráficos
    """
    
    # Eliminar NaNs
    df_datos_de_la_sonda = df_datos_de_la_sonda.dropna(subset=["tspan_de_envio"]) 
    
     # Obtener posiciones iniciales del excel de despliegue
    lat_ini = df_datos_de_la_sonda["latitud"].iloc[0]
    lon_ini = df_datos_de_la_sonda["longitud"].iloc[0]
    
    # Obtener posiciones y rapidez de corriente del periodo de estudio
    latitud_estudio = df_datos_de_la_sonda['latitud']
    longitud_estudio = df_datos_de_la_sonda['longitud']   
    rap_corriente_estudio = df_datos_de_la_sonda['rap_corriente']
    
    
    # Posición final
    lat_fin = latitud_estudio.iloc[-1]
    lon_fin = longitud_estudio.iloc[-1]
    
    obj_mapeable = plt.scatter(longitud_estudio, 
                               latitud_estudio, 
                               c=rap_corriente_estudio, 
                               cmap="jet", 
                               s=10, 
                               vmin=0, vmax=1.5, 
                               transform=ccrs.PlateCarree())
    
    if graficar_trayectorias_pasadas and df_datos_previos_de_la_sonda is not None:
        df_datos_previos_de_la_sonda = df_datos_previos_de_la_sonda.dropna(subset=["tspan_de_envio"])
        latitud_pasada = df_datos_previos_de_la_sonda['latitud']
        longitud_pasada = df_datos_previos_de_la_sonda['longitud']
        plt.scatter(longitud_pasada, latitud_pasada, c='black', linestyle='--', s=1, transform=ccrs.PlateCarree())
        # plt.plot(longitud_pasada, latitud_pasada, linestyle='--', color='black', marker='', linewidth=1.5, transform=ccrs.PlateCarree())

        lat_ini = df_datos_previos_de_la_sonda["latitud"].iloc[0]
        lon_ini = df_datos_previos_de_la_sonda["longitud"].iloc[0]

    print(f"sonda {serial} lat ini= {lat_ini}, lon ini= {lon_ini}")

    plt.scatter([lon_ini], [lat_ini], c='yellow', edgecolors='black', linewidths=2, s=50, transform=ccrs.PlateCarree())
    plt.scatter([lon_fin], [lat_fin], c='red', edgecolors='black', linewidths=2, s=50, transform=ccrs.PlateCarree())
    
    return obj_mapeable
        
    