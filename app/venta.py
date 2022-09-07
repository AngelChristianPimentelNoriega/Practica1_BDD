class Venta():
    """
        Clase Ventas, contiene los atributos de una venta
    """
    def __init__(self, data):
        """	
        Constructor de la clase Venta, recibe una serie de datos
        """
        self.id_medicamento = data['id_medicamento']
        self.dia = data['dia']
        self.mes = data['mes']
        self.año = data['año']
        self.total = data['total']

    def __str__(self):
        """	
        Metodo que devuelve una cadena de texto con los atributos de la venta
        """
        return f'ID Medicamento: {self.id_medicamento}, Dia: {self.dia}, Mes: {self.mes}, Año: {self.año}, Total: {self.total}'
    
    def to_dict(self):
        """
        Metodo que devuelve un diccionario con los atributos de la venta
        """
        return {
            'id_medicamento': self.id_medicamento,
            'dia': self.dia,
            'mes': self.mes,
            'año': self.año,
            'total': self.total
        }