Trabajo final de PDyTR
Para windows: Set-ExecutionPolicy RemoteSigned –Scope Process
Para testear si funciona gRPC
git clone -b v1.66.0 --depth 1 --shallow-submodules https://github.com/grpc/grpc
cd grpc/examples/python/helloworld
server:python greeter_server.py
cliente:python greeter_client.py
----------------- Proyecto -----------------
Situar la terminal en el directorio flotas y ejecutar:
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. vehiculos.proto

Ejecutar servidor dashboard python manage.py runserver

