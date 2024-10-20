import grpc
from django.shortcuts import render
from google.protobuf.empty_pb2 import Empty
import vehiculos_pb2
import vehiculos_pb2_grpc

def panel_control(request):
    """Vista para mostrar el panel de control de vehículos."""
    vehiculos_data = []
    
    # Realiza la conexión al servidor gRPC
    with grpc.insecure_channel('localhost:50051') as canal:
        cliente = vehiculos_pb2_grpc.VehiculosServiceStub(canal)
        try:
            # Solicita el estado de los vehículos
            respuesta = cliente.ObtenerEstadoVehiculos(Empty())
            vehiculos_data = [{"id": vehiculo.id, "data": vehiculo.json_data} for vehiculo in respuesta.vehiculos]
        except grpc.RpcError as e:
            print(f"Error al llamar al servidor gRPC: {e.details()}")
            # Manejo de errores según sea necesario
            
    # Renderiza la plantilla con los datos de los vehículos
    return render(request, 'dashboard.html', {'vehiculos': vehiculos_data})
