# TODO: [global] replace print with varying levels of logging
# TODO: catch all possible and not possible exceptions
# TODO: set the socket timeouts by hand
# TODO: add command line parameters:
#       - name of the config to load
#       - number of entire code cycle repeats
import socket
from cfg.loader import get_configs

config = get_configs('test')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listen_socket:
    listen_socket.bind((config['listen_address'], config['port']))
    print(f'##listen on {config["listen_address"]}:{config["port"]}')
    listen_socket.listen()
    while True:
        print('..wait for incoming connections')
        client_socket, client_address = listen_socket.accept()
        print(f'<-catch new connection from {client_address}')
        with client_socket:
            if client_address[0] not in config['allowed_hosts']:
                print('!!reject connection from host not in whitelist')
            else:
                for response_row in config['data_rows']:
                    print('..listen for data from current connection')
                    recv_data = client_socket.recv(1024)  # or lower\higher?
                    print(f'<-{recv_data} received from the current connection')
                    # TODO: do some checks and transformation to the data sent back
                    client_socket.sendall(response_row)  # might throw the errno32 broken pipe
                    print(f'->{response_row=} sent to the client')
                break
    print('##no data left, stop the server, close the listening socket')
