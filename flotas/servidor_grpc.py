import grpc
from concurrent import futures
import json
import time
import vehiculos_pb2
import vehiculos_pb2_grpc

class VehiculosService(vehiculos_pb2_grpc.VehiculosServiceServicer):
    def __init__(self):
        self.datos_vehiculos = []  # Almacena los datos de los vehículos

    def ActualizarVehiculo(self, request_iterator, context):
        """Recibe datos de vehículos en formato JSON."""
        print("Esperando datos de vehículos...")
        for datos_json in request_iterator:
            print(f"Datos JSON recibidos: {datos_json.json_data}")
            # Convertir el JSON recibido a un diccionario
            try:
                datos = json.loads(datos_json.json_data)
                self.datos_vehiculos.append(datos)  # Almacena los datos recibidos como dict
            except json.JSONDecodeError:
                context.set_details("Error al decodificar el JSON")
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                return vehiculos_pb2.Respuesta(status="Error al decodificar JSON")

        return vehiculos_pb2.Respuesta(status="Datos recibidos correctamente")

    def ObtenerEstadoVehiculos(self, request, context):
        """Devuelve el estado de todos los vehículos."""
        estado = vehiculos_pb2.EstadoVehiculos()
        for vehiculo in self.datos_vehiculos:
            estado.vehiculos.add(id=vehiculo['id'], json_data=json.dumps(vehiculo))
        return estado

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    vehiculos_pb2_grpc.add_VehiculosServiceServicer_to_server(VehiculosService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor gRPC escuchando en el puerto 50051...")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
