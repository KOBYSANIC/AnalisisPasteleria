from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
import random
from datetime import datetime, timedelta


def inicio(request):
    # Obtiene la lista de pasteles
    with connection.cursor() as cursor:
        cursor.execute("SELECT ID_Pastel ,Nombre, Precio, Familia FROM Pastel")
        pasteles_data = cursor.fetchall()

    pasteles = []
    for pastel_data in pasteles_data:
        ID_pastel = pastel_data[0]
        nombre_pastel = pastel_data[1]
        precio_pastel = pastel_data[2]
        nombre_imagen = f"static/img/{nombre_pastel}.jpg"  # Utiliza la carpeta 'img'
        pastel = {'ID_Pastel': ID_pastel ,'Nombre': nombre_pastel, 'Imagen_URL': nombre_imagen ,'Precio': precio_pastel, 'Familia': pastel_data[3]}
        pasteles.append(pastel)

    # Obtiene la lista de familias
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT Familia FROM Pastel")
        familias_data = cursor.fetchall()

    familias = [familia[0] for familia in familias_data]

    return render(request, 'catalogo.html', {'pasteles': pasteles, 'familias': familias})


def obtener_descripcion_pastel(request):
    if request.method == 'GET':
        pastel_id = request.GET.get('pastel_id')
        print (pastel_id)

        with connection.cursor() as cursor:
            cursor.execute("SELECT Descripcion FROM Pastel WHERE ID_Pastel = %s", [pastel_id])
            result = cursor.fetchone()

            if result is not None:
                descripcion = result[0]
                return JsonResponse({'descripcion': descripcion})
            else:
                # Manejar el caso en el que no se encuentra un pastel con el ID especificado
                return JsonResponse({'descripcion': 'Pastel no encontrado'})

def obtener_ingredientes_pastel(request):
    if request.method == 'GET':
        pastel_id = request.GET.get('pastel_id')
        print (pastel_id)

        with connection.cursor() as cursor:
            cursor.execute("SELECT Ingredientes FROM Pastel WHERE ID_Pastel = %s", [pastel_id])
            result = cursor.fetchone()

            if result is not None:
                ingredientes = result[0]
                return JsonResponse({'ingredientes': ingredientes})
            else:
                # Manejar el caso en el que no se encuentra un pastel con el ID especificado
                return JsonResponse({'ingredientes': 'No hay ingredientes'})
            
def obtener_pasteles_disponibles(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT ID_Pastel, Nombre FROM Pastel")
        pasteles = cursor.fetchall()

    return render(request, 'catalogo.html', {'pasteles': pasteles})

def procesar_pedido(request):
    from datetime import datetime

    fecha_actual = datetime.now()

    if request.method == 'POST':
        # Captura los datos del formulario
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        tipo_pago = request.POST.get('tipo_pago')
        saldo = request.POST.get('saldo')
        pastel_id = request.POST.get('pastel_id')

        try:
        # Realiza la inserción en la base de datos utilizando una consulta SQL
            with connection.cursor() as cursor:
                Id_cliente = random.randint(100000, 999999)
                fecha_actual = None  # Inicializa la variable

                if tipo_pago == "Contado":
                    fecha_actual = datetime.now().strftime('%Y-%m-%d')

                if tipo_pago == "Credito":
                    # Obtiene la fecha actual
                    Actual = datetime.now()

                    # Suma 30 días a la fecha actual para pagar la deuda
                    fecha_en_30_dias = Actual + timedelta(days=30)

                    # Convierte la fecha en un formato específico (por ejemplo, 'YYYY-MM-DD')
                    fecha_actual = fecha_en_30_dias.strftime('%Y-%m-%d')

                sql = """
                    INSERT INTO Pedidos_Cliente (ID_Cliente, nombre, direccion, telefono, tipo_pago, Saldo, fecha_de_cobro, ID_Pastel) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (Id_cliente, nombre, direccion, telefono, tipo_pago, saldo, fecha_actual, pastel_id))

                # Realiza un commit para guardar los cambios
                connection.commit()

        except Exception as e:
            #Captura y devuelve el error en formato JSON
            error_message = f'Error: {str(e)}'
            return JsonResponse({'error': error_message}, status=400)

    return JsonResponse({'message': 'Solicitud válida'}, status=200)

def cocinar_pastel(request):
    if request.method == 'POST':
        # Captura los datos del formulario
        ID_pastel = request.POST.get('ID_Pastel')
        nombre = request.POST.get('nombre')
        porciones = request.POST.get('porciones')
        familia = request.POST.get('familia')
        descripcion = request.POST.get('descripcion')
        ingredientes = request.POST.get('ingredientes')
        precio = request.POST.get('precio')

        try:
            # Realiza la inserción en la base de datos utilizando una consulta SQL
            with connection.cursor() as cursor:
                sql = """
                    INSERT INTO Pastel (ID_Pastel, Nombre, Porciones, Familia, Descripcion, Ingredientes, Precio, Hora_creado)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, FORMAT(GETDATE(), 'hh:mm tt'))
                """
                cursor.execute(sql, (ID_pastel, nombre, porciones, familia, descripcion, ingredientes, precio))

            return JsonResponse({'message': 'Pastel cocinado con éxito'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

from django.shortcuts import render
from django.http import HttpResponseRedirect
import datetime
from django.db import connection

def aplicar_rebaja(request):
    if request.method == 'POST':
        # Obtén la hora actual 
        hora_actual = datetime.datetime.now().time()

        # Crear una consulta SQL que disminuye el precio de los pasteles creados antes de la hora actual.
        sql = """
            UPDATE Pastel
            SET Precio = Precio * 0.9
            WHERE Hora_creado < %s
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, [hora_actual])

        # Redirige a la página de control de precio actualizada
        return HttpResponseRedirect('/control_precio/')  # Ajusta la URL según tu configuración


def control_precio(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT ID_Pastel, Nombre, Porciones, Familia, Descripcion, Ingredientes, Precio, Hora_creado FROM Pastel")
        Precio_content = cursor.fetchall()

    return render(request, 'Control_precio.html', {'Precio_content': Precio_content})

def realizar_pedido(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT ID_Cliente, nombre, direccion, telefono, tipo_pago, saldo, fecha_de_cobro, ID_Pastel FROM Pedidos_Cliente")
        Pedidos_content = cursor.fetchall()

    return render(request, 'Pedidos.html', {'Pedidos_content': Pedidos_content})
