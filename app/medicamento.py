class Medicamento():
    """
    	Clase Medicamento, contiene los atributos de un medicamento

    """
    # Posibles categorias de medicamentos
    categorias = ["Antibioticos","Desinflamantes","Analgesicos","Alimentos","Bebidas","Otros"]
    
    def __init__(self, data):
        """	
        Constructor de la clase Medicamento
        """ 
        self.id = data['id']
        self.nombre = data['nombre']
        if data['categoria'] in self.categorias:
            self.categoria = data['categoria']
        else:
            raise ValueError('Categoria no valida')
        self.precio = data['precio']
        self.stock = data['stock']
    
    def __str__(self) -> str:
        """
        Metodo que devuelve una cadena de texto con los atributos del medicamento
        """
        return f'ID: {self.id}, Nombre: {self.nombre}, Categoria: {self.categoria}, Precio: {self.precio}, Stock: {self.stock}'
    
    def to_dict(self):
        """
        Metodo que devuelve un diccionario con los atributos del medicamento
        """ 
        return {
            'id': self.id,
            'nombre': self.nombre,
            'categoria': self.categoria,
            'precio': self.precio,
            'stock': self.stock
        }