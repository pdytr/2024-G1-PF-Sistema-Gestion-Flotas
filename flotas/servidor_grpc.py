import grpc
from concurrent import futures
from vehiculos_pb2 import Respuesta
import vehiculos_pb2_grpc

class VehiculoService(vehiculos_pb2_grpc.VehiculoServiceServicer):
    def EnviarDatosFlujo(self, request_iterator, context):
        for datos in request_iterator:
            print(f"[{datos.id_vehiculo}] Ubicación: ({datos.latitud}, {datos.longitud})")
            print(f"  Velocidad: {datos.velocidad} km/h | Combustible: {datos.nivel_combustible}%")
            print(f"  Batería: {datos.nivel_bateria}%\n")
        return Respuesta(mensaje="Datos recibidos correctamente")

def servir():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    vehiculos_pb2_grpc.add_VehiculoServiceServicer_to_server(VehiculoService(), server)
    server.add_insecure_port('[::]:50051')
    print("Servidor gRPC ejecutándose en el puerto 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    servir()
