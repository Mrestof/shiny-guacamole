# TODO: catch all possible and not possible exceptions
# TODO: replace print with varying levels of logging
# TODO: structure the code a bit more fine
import socket
from config import Test as Config

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listen_socket:
    listen_socket.bind((Config.listen_address, Config.port))
    print(f'##listen on {Config.listen_address}:{Config.port}')
    listen_socket.listen()
    for response_row in Config.data_rows:
        print(f'##prepare next response row to reply with: {response_row = }')
        while True:
            print('..wait for incoming connections')
            client_socket, client_address = listen_socket.accept()
            print(f'<-catch new connection from {client_address}')
            with client_socket:
                if client_address[0] in Config.allowed_hosts:
                    client_socket.sendall(response_row)
                    print(f'->send the response row to the client')
                    break
                # else
                print('!!reject connection from host not in whitelist')
