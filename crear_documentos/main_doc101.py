from services.doc_101.orquestador import generar_documento_101


if __name__ == "__main__":
    from configs.configuracion_101 import doc_config
    generar_documento_101(doc_config)
    
else:
    print("Ejecutandose desde otro módulo")