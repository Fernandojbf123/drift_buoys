import pandas as pd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np

def graficar_trayectorias_de_sonda(df_excel_de_despliegue: pd.DataFrame, serial: str, df_datos_de_la_sonda: pd.DataFrame):
    # Obtener posiciones iniciales del excel de despliegue
    lat_ini_series = df_excel_de_despliegue[df_excel_de_despliegue['serie_de_sonda'] == serial]['latitud_de_despliegue']
    lon_ini_series = df_excel_de_despliegue[df_excel_de_despliegue['serie_de_sonda'] == serial]['longitud_de_despliegue']
    lat_ini = float(lat_ini_series.iloc[0]) if not lat_ini_series.empty else None
    lon_ini = -float(lon_ini_series.iloc[0]) if not lon_ini_series.empty else None
        
    # Obtener posiciones y rapidez de corriente del diccionario de datos
    
    latitud = df_datos_de_la_sonda['latitud']
    longitud = df_datos_de_la_sonda['longitud']   
    rap_corriente = df_datos_de_la_sonda['rap_corriente']
    lat_fin = latitud.iloc[-1]
    lon_fin = longitud.iloc[-1]
    
    obj_mapeable = plt.scatter(longitud, latitud, c=rap_corriente, cmap="jet", s=10, vmin=0, vmax=1.5, transform=ccrs.PlateCarree())
    plt.scatter([lon_ini], [lat_ini], c='yellow', edgecolors='black', linewidths=2, s=50, transform=ccrs.PlateCarree())
    plt.scatter([lon_fin], [lat_fin], c='red', edgecolors='black', linewidths=2, s=50, transform=ccrs.PlateCarree())
    
    return obj_mapeable
        
    