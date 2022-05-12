# TODO: [global] replace print with varying levels of logging
# TODO: catch all possible and not possible exceptions
# TODO: set the socket timeouts by hand
# TODO: add command line parameters:
#       - name of the config to load
#       - number of entire code cycle repeats
import socket
from sys import argv
from time import sleep
from typing import Dict, Any, Tuple
from cfg.loader import get_configs


def parse_args() -> Tuple[Dict[str, Any], int]:
    usage = f'usage: {argv[0]!r} [--help] <config_name.ini> [amount_of_clients_to_process]'
    try:
        if argv[1] == '--help':
            print(usage)
            exit(0)
        # file existing is handled by `loader`
        config = get_configs(argv[1])
    except IndexError:
        raise SystemExit(f'!!{usage}')
    try:
        client_amount = int(argv[2])
    except IndexError:
        client_amount = 1
    except ValueError:
        raise SystemExit(f'!!passed {argv[2]!r} as the `amount_of_clients_to_process`, it must be an integer')
    return config, client_amount


def process_client(config: Dict[str, Any]) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listen_socket:
        # TODO: here we are catching `OSError: Address already in use`
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
                if potential_handshake != config['handshake'][0]:
                    print('!!reject handshake: it described differently in config')
                    continue
                handshake_response = config['handshake'][1]
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
                        print('##sleep for 300ms')
                        sleep(0.3)
                        client_socket.sendall(reply)  # might throw the errno32 broken pipe
                        print(f'->"{reply}" sent to the client')
                break


def main() -> None:
    config, client_amount = parse_args()
    print('##start the server')
    while client_amount != 0:
        print('##process new client')
        process_client(config)
        client_amount -= 1
    print('##stop the server')


if __name__ == '__main__':
    main()
