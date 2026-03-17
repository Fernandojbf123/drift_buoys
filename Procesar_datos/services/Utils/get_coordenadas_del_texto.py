def get_coordenadas_del_texto(longitud, latitud, texto):
    lon_txt = longitud + 0.05
    lat_txt = latitud + 0.007
    
    if "nuevo campechito" in texto.lower():
        lon_txt = longitud-0.4
        lat_txt = latitud-0.05
    elif "sánchez" in texto.lower():
        lon_txt = longitud-0.4
        lat_txt = latitud-0.05
    elif "isla aguada" in texto.lower():
        lon_txt = longitud-0.4
        lat_txt = latitud-0.05
        
    return lon_txt, lat_txt