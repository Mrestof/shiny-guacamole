# TODO: cover the code with exceptions
# TODO: expand the test:
#       - test to connect with forbidden address
#       - test to overtime the connection
# TODO: add command line parameters:
#       - list of tests to accomplish
# TODO: make test not relying on `data_rows` config (by sending as many packets as server allows)
import socket
from cfg.loader import get_configs

config = get_configs('cfg/test.ini')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tx_sock:
    print('##start test')
    host = '127.0.0.1', config['port']
    tx_sock.connect(host)
    print(f'->connect to the host: {host}')
    for _ in config['data_rows']:
        tx_data = b'rawr~'
        tx_sock.sendall(tx_data)
        print(f'->{tx_data} sent to the current connection')
        print('..wait for a response')
        response = tx_sock.recv(1024)
        print(f'<-{response} received from current connection')
    print('##finish test')
