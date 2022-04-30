# TODO: [global] replace print with varying levels of logging
# TODO: catch all possible and not possible exceptions
# TODO: set the socket timeouts by hand
# TODO: add command line parameters:
#       - name of the config to load
#       - number of entire code cycle repeats
import socket
from cfg.loader import get_configs

config = get_configs('cfg/test.ini')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listen_socket:
    listen_socket.bind((config['listen_address'], config['port']))
    print(f'##listen on {config["listen_address"]}:{config["port"]}')
    listen_socket.listen()
    while True:
        print('..listen for incoming connections')
        client_socket, client_address = listen_socket.accept()
        print(f'<-catch new connection from {client_address}')
        with client_socket:
            if client_address[0] not in config['allowed_hosts']:
                print('!!reject connection from host not in whitelist')
                continue
            print('..listen for incoming handshake')
            potential_handshake = client_socket.recv(1024)
            print(f'<-"{potential_handshake} received potential handshake from the current connection')
            if potential_handshake not in config['handshake']:
                print('!!reject handshake: it described differently in config')
                continue
            handshake_response = config['handshake'][potential_handshake]
            client_socket.sendall(handshake_response)
            print(f'->"{handshake_response}" send handshake response')
            while True:
                print('..listen for incoming data from current connection')
                recv_data = client_socket.recv(1024)  # or lower\higher?
                print(f'<-"{recv_data}" received from the current connection')
                if not recv_data:
                    print(f'##the client has closed the connection, closing it too')
                    break
                if recv_data not in config['data_rows']:
                    print(f'##no replies found in config')
                    continue
                for reply in config['data_rows'][recv_data]:
                    client_socket.sendall(reply)  # might throw the errno32 broken pipe
                    print(f'->"{reply }" sent to the client')
            break
    print('##stop the server')
