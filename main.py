#Practica 01 
# Autor Andrea Fernanda Reyes Farfan
# Fecha: 2021-09-20
# Version: 1.0


import pandas as pd

from pathlib import Path

from app.medicamento import Medicamento
from app.venta import Venta



def existen_registros():
    """Verifica si existe el directorio de registros y los archivos de medicamentos y ventas"""
    directory = Path('./registros')
    if not directory.exists():
        directory.mkdir()
    ventas = Path('./registros/ventas.csv')
    medicamentos = Path('./registros/medicamentos.csv')
    if not ventas.exists():
        ventas.touch()
    if not medicamentos.exists():
        medicamentos.touch()

def existe_medicamento(lista_medicamento ,medicamento):
    """
    Verifica si el medicamento ya existe en la lista
    @return True si existe, False si no existe
    """	
    for m in lista_medicamento:
        if m.id == medicamento['id'] or m.nombre == medicamento['nombre']:
            return True
    return False

def buscar_medicamento_nombre(nombre):
    """Busca un medicamento por su nombre
    @return Medicamento si existe, None si no existe
    """	
    lista_medicamento = leer_medicamentos_existentes()
    for medicamento in lista_medicamento:
        if medicamento.nombre == nombre:
            return medicamento
    return None

def buscar_medicamento_id(id):
    """Busca un medicamento por su id
    @return Medicamento si existe, None si no existe
    """
    lista_medicamento = leer_medicamentos_existentes()
    for medicamento in lista_medicamento:
        if medicamento.id == id:
            return medicamento
    return None

def buscar_medicamento_categoria(categoria):
    """Busca un medicamento por su categoria
        @return Medicamento si existe, None si no existe
    """
    lista_medicamento = leer_medicamentos_existentes()
    lista_categoria = []
    for medicamento in lista_medicamento:
        if medicamento.categoria == categoria:
            lista_categoria.append(medicamento)
    return lista_categoria

def leer_medicamentos_existentes():
    """Lee los medicamentos existentes en el archivo de medicamentos
    @return lista de medicamentos
    """	
    medicamentos = pd.read_csv('./registros/medicamentos.csv')
    lista_medicamento = []
    for index, row in medicamentos.iterrows():
        try:
            if not existe_medicamento(lista_medicamento, row):
                lista_medicamento.append(Medicamento(row))
        except KeyError as e:
            print(row)
    return lista_medicamento

def leer_ventas_existentes():
    """Lee las ventas existentes en el archivo de ventas
        @return lista de ventas
    """
    ventas = pd.read_csv('./registros/ventas.csv')
    lista_ventas = []
    for index, row in ventas.iterrows():
        try:
            lista_ventas.append(Venta(row))
        except KeyError as e:
            print(row)
    return lista_ventas

def obtener_ultimo_id(lista_medicamento):
    """Obtiene el ultimo id de la lista de medicamentos
        @return ultimo id
    """
    if len(lista_medicamento) == 0:
        return 0
    id_maximo = 0
    for medicamento in lista_medicamento:
        if medicamento.id > id_maximo:
            id_maximo = medicamento.id
    return id_maximo

def registrar_medicamento():
    """Registra un medicamento en el archivo de medicamentos
        @return True si se registro, False si no se registro
    """	
    lista_medicamento = leer_medicamentos_existentes()
    medicamento = {}
    medicamento['id'] = obtener_ultimo_id(lista_medicamento) + 1
    medicamento['nombre'] = input('Ingrese el nombre del medicamento: ')
    print('Las categorias disponibles son: Antibioticos, Desinflamantes, Analgesicos, Alimentos, Bebidas, Otros')
    medicamento['categoria'] = input('Ingrese la categoria del medicamento: ')
    try:
        medicamento['precio'] = float(input('Ingrese el precio del medicamento: '))
        medicamento['stock'] = int(input('Ingrese el stock del medicamento: '))
    except ValueError as e:
        print('El precio y el stock deben ser valores numericos')
        return False
    try:
        lista_medicamento.append(Medicamento(medicamento))
    except ValueError as e:
        print(e)
        return False
    nueva_lista = []
    for medicamento in lista_medicamento:
        nueva_lista.append(medicamento.to_dict())
    df = pd.DataFrame(nueva_lista)
    df.to_csv('./registros/medicamentos.csv', index=False)
    return True

def actualizar_medicamento(medicamento):
    """Actualiza un medicamento en el archivo de medicamentos
    """
    lista_medicamento = leer_medicamentos_existentes()
    for i in range(len(lista_medicamento)):
        if lista_medicamento[i].id == medicamento.id:
            lista_medicamento[i] = medicamento
    nueva_lista = []
    for medicamento in lista_medicamento:
        nueva_lista.append(medicamento.to_dict())
    df = pd.DataFrame(nueva_lista)
    df.to_csv('./registros/medicamentos.csv', index=False)

def registrar_venta():
    """Registra una venta en el archivo de ventas
    @return True si se registro, False si no se registro
    """
    venta = {}
    try:
        venta['dia'] = int(input('Ingrese el dia de la venta: '))
        if venta['dia'] < 1 or venta['dia'] > 31:
            print('El dia debe estar entre 1 y 31')
            return False
        venta['mes'] = int(input('Ingrese el mes de la venta: '))
        if venta['mes'] < 1 or venta['mes'] > 12:
            print('El mes debe estar entre 1 y 12')
            return False
        venta['año'] = int(input('Ingrese el año de la venta: '))
        if venta['año'] > 2022:
            print('El año debe ser menor o igual a 2022')
            return False
        nombre = input('Ingrese el nombre del medicamento: ')
        try:
            cantidad = int(input('Ingrese la cantidad de medicamentos vendidos: '))
        except ValueError as e:
            print('La cantidad debe ser un valor numerico')
            return False
        medicamento_buscado = buscar_medicamento_nombre(nombre)
        if medicamento_buscado is None:
            print('No existe el medicamento')
            return False
        if medicamento_buscado.stock < cantidad:
            print('No hay suficiente stock')
            return False
        else:
            medicamento_buscado.stock -= cantidad
            actualizar_medicamento(medicamento_buscado)
        venta['total'] = medicamento_buscado.precio * cantidad
        venta['id_medicamento'] = medicamento_buscado.id
    except ValueError as e:
        print('El dia, mes, año y total deben ser valores numericos')
        return False
    lista_ventas = leer_ventas_existentes()
    lista_ventas.append(Venta(venta))
    nueva_lista = []
    for venta in lista_ventas:
        nueva_lista.append(venta.to_dict())
    df = pd.DataFrame(nueva_lista)
    df.to_csv('./registros/ventas.csv', index=False)
    return True


if __name__ == "__main__":
    try:
        print('Iniciando programa...')
        existen_registros()
        print('Obteniendo medicamentos y ventas...')
        while True:
            print('1. Registrar medicamento')
            print('2. Registrar venta')
            print('3. Ver medicamentos')
            print('4. Ver ventas')
            print('5. Buscar medicamento')
            print('6. Salir')
            opcion = input('Ingrese una opción: ')
            if opcion == '1':
                print('Registrando medicamento...')
                if registrar_medicamento():
                    print('Medicamento registrado correctamente')
                else:
                    print('Error al registrar medicamento')
            elif opcion == '2':
                print('Registrando venta...')
                if registrar_venta():
                    print('Venta registrada correctamente')
                else:
                    print('Error al registrar venta')
            elif opcion == '3':
                print('Ver medicamentos...')
                for m in leer_medicamentos_existentes():
                    print(m)
            elif opcion == '4':
                print('Ver ventas...')
                for v in leer_ventas_existentes():
                    print(v)
            elif opcion == '5':
                print('Buscar medicamento...')
                while True:
                    print('1. Buscar por nombre')
                    print('2. Buscar por categoria')
                    print('3. Buscar por id')
                    print('4. Salir')
                    opcion = input('Ingrese una opción: ')
                    if opcion == '1':
                        print('Buscando por nombre...')
                        nombre = input('Ingrese el nombre del medicamento: ')
                        medicamento = buscar_medicamento_nombre(nombre)
                        if medicamento is None:
                            print('No existe el medicamento')
                        else:
                            print(medicamento)
                    elif opcion == '2':
                        print('Buscando por categoria...')
                        categoria = input('Ingrese la categoria del medicamento: ')
                        medicamentos = buscar_medicamento_categoria(categoria)
                        if len(medicamentos) == 0:
                            print('No existen medicamentos con esa categoria')
                        else:
                            for m in medicamentos:
                                print(m)
                    elif opcion == '3':
                        print('Buscando por id...')
                        try:
                            id = int(input('Ingrese el id del medicamento: '))
                        except ValueError as e:
                            print('El id debe ser un valor numerico')
                            continue
                        medicamento = buscar_medicamento_id(id)
                        if medicamento is None:
                            print('No existe el medicamento')
                        else:
                            print(medicamento)
                    elif opcion == '4':
                        break
            elif opcion == '6':
                print('Saliendo...')
                break
            else:
                print('Opción no válida')
    except KeyboardInterrupt as e:
        print('Saliendo...')
        exit()


    