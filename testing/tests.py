# TODO: cover the code with exceptions
# TODO: expand the test:
#       - test to connect with forbidden address
#       - test to overtime the connection
import socket
from cfg.loader import get_configs

config = get_configs('cfg/test.ini')


def full(server_addr: str = '127.0.0.1') -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tx_sock:
        print('##start full test')
        host = server_addr, config['port']
        tx_sock.connect(host)
        print(f'->connect to the host: {host}')
        cfg_handshake_tx, cfg_handshake_rx = config['handshake']
        tx_sock.sendall(cfg_handshake_tx)
        print(f'->{cfg_handshake_tx} handshake sent to the current connection')
        print(f'..wait for a handshake response')
        handshake_rx = tx_sock.recv(64)
        print(f'<-{handshake_rx} received potential handshake from current connection')
        if handshake_rx != cfg_handshake_rx:
            print(f'!!{handshake_rx} != {cfg_handshake_rx}: reject incorrect handshake response')
            return False
        for cfg_tx, cfg_rx in config['data_rows'].items():
            tx_sock.sendall(cfg_tx)
            print(f'->{cfg_tx} sent to the current connection')
            print(f'##amount of packages to receive: {len(cfg_rx)}')
            for part in cfg_rx:
                print(f'..wait for a response')
                response = tx_sock.recv(64)
                print(f'<-{response} received from current connection')
                if response != part:
                    print(f'!!{response} != {part}: response is not what expected')
                    return False
        print('##finish test')
    return True
