import grpc
from django.shortcuts import render
from google.protobuf.empty_pb2 import Empty
import vehiculos_pb2
import vehiculos_pb2_grpc
import json
from django.http import JsonResponse
def panel_control(request):
    """Vista para mostrar el panel de control de vehículos."""
    vehiculos_data = []
    alertas = []  # Lista para almacenar alertas
    vehiculos_pos = []
    # Realiza la conexión al servidor gRPC
    with grpc.insecure_channel('localhost:50051') as canal:
        cliente = vehiculos_pb2_grpc.VehiculosServiceStub(canal)
        try:
            respuesta = cliente.ObtenerEstadoVehiculos(Empty())

            for vehiculo in respuesta.vehiculos:
                ve = json.loads(vehiculo.json_data)
                vehiculos_pos.append({
                    "id": ve["id"], 
                    "latitud": ve["latitud"], 
                    "longitud": ve["longitud"],
                    "combustible":ve["nivel_combustible"],
                    "bateria":ve["nivel_bateria"],
                })
                vehiculos_data.append({
                    "id": ve["id"], 
                    "latitud": ve["latitud"], 
                    "longitud": ve["longitud"],
                    "data": vehiculo.json_data
                })
                

                if ve["nivel_combustible"] < 15:
                    alertas.append(f"Alerta: Bajo nivel de combustible en el vehículo {ve["id"]}.")
                if ve["nivel_bateria"] < 15:
                    alertas.append(f"Alerta: Bajo nivel de bateria en el vehículo {ve["id"]}.")

        except grpc.RpcError as e:
            print(f"Error al llamar al servidor gRPC: {e.details()}")
            
    # Renderiza la plantilla con los datos de los vehículos y alertas
    return render(request, 'dashboard.html', {'vehiculos': vehiculos_data, 'alertas': alertas,"vehiculosPos":json.dumps(vehiculos_pos)})
def actualizar_datos_vehiculos(request):
    """Función para actualizar los datos de los vehículos."""
    if request.method == "GET":
        vehiculos_pos = []
        # Realiza la conexión al servidor gRPC
        with grpc.insecure_channel('localhost:50051') as canal:
            cliente = vehiculos_pb2_grpc.VehiculosServiceStub(canal)
            try:
                respuesta = cliente.ObtenerEstadoVehiculos(Empty())
                for vehiculo in respuesta.vehiculos:
                    ve = json.loads(vehiculo.json_data)
                    vehiculos_pos.append({
                        "id": ve["id"], 
                        "latitud": ve["latitud"], 
                        "longitud": ve["longitud"],
                        "combustible": ve["nivel_combustible"],
                        "bateria": ve["nivel_bateria"],
                    })
            except grpc.RpcError as e:
                print(f"Error al llamar al servidor gRPC: {e.details()}")

        # Devuelve los datos en formato JSON
        return JsonResponse(vehiculos_pos, safe=False)
