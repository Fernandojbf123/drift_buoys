from src.revisor_de_doris_duplicadas import revisor_de_doris_duplicadas

if __name__ == "__main__":
    from configs.configuracion_general import config_verificacion
    import configs.manager_configuracion as manager_configuracion
        
    config = manager_configuracion.Configs(config_verificacion)
    revisor_de_doris_duplicadas(config)

else:
    print("corriendo desde el módulo principal")
    pass
