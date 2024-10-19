import grpc
import vehiculos_pb2
import vehiculos_pb2_grpc
import time
import random
import threading

def generar_datos_vehiculo(id_vehiculo):
    while True:
        yield vehiculos_pb2.DatosVehiculo(
            id_vehiculo=id_vehiculo,
            latitud=random.uniform(-90, 90),
            longitud=random.uniform(-180, 180),
            velocidad=random.uniform(0, 120),
            nivel_combustible=random.uniform(0, 100),
            nivel_bateria=random.uniform(0, 100)
        )
        time.sleep(2)  # Envía datos cada 2 segundos

def enviar_datos_vehiculo(id_vehiculo):
    with grpc.insecure_channel('localhost:50051') as canal:
        cliente = vehiculos_pb2_grpc.VehiculoServiceStub(canal)
        respuesta = cliente.EnviarDatosFlujo(generar_datos_vehiculo(id_vehiculo))
        print(f"Respuesta del servidor para {id_vehiculo}: {respuesta.mensaje}")

def ejecutar_clientes():
    # Creo dos hilos, uno por cada vehículo.
    vehiculo_1 = threading.Thread(target=enviar_datos_vehiculo, args=("V123",))
    vehiculo_2 = threading.Thread(target=enviar_datos_vehiculo, args=("V456",))

    # Inicializo los hilos para que envíen datos en paralelo.
    vehiculo_1.start()
    vehiculo_2.start()


    vehiculo_1.join()
    vehiculo_2.join()

if __name__ == '__main__':
    ejecutar_clientes()
