

class Configs():
    def __init__(self, config):
        self.config = config

    # acceder a cualquier atributo con get
    def get(self, attribute_name):
        return self.config.get(attribute_name)
    
    # acceder a cualquier atributo directamente como propiedad
    def __getattr__(self, attribute_name):
        return self.config.get(attribute_name)
    
    # acceder a cualquier atributo como si fuera un diccionario
    def __getitem__(self, attribute_name):
        return self.config.get(attribute_name)
    