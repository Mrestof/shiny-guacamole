from os.path import isfile
from socket import inet_pton, AF_INET
from typing import Dict, List, Tuple, Any
from configparser import ConfigParser

CFG_DEF_SECT = 'main'


def port_guard(conf_value: str) -> int:
    """Check and transform the string port value to the integer one"""
    try:
        port = int(conf_value)
    except ValueError:
        raise SystemExit(f'!!port must be an integer, passed value is {conf_value}')
    assert 2**10 < port < 2**16, '!!port is in dangerous or is in forbidden range'
    return port


def listen_address_guard(conf_value: str) -> str:
    """Check and return the string listen_address value"""
    if conf_value == '':  # empty address tells the server to bind to every interface
        return conf_value
    try:
        inet_pton(AF_INET, conf_value)
    except OSError:
        raise SystemExit(f'!!listen address must be a full IPv4 formatted string, passed value is {conf_value}')
    return conf_value


def handshake_guard(conf_value: str) -> Tuple[bytes, bytes]:
    """Check and transform the string handshake value to the tuple of response on specific handshake"""
    handshake_pair = tuple()
    try:
        data_in, data_out = conf_value.split(':')
        data_in_bin, data_out_bin = bytes.fromhex(data_in), bytes.fromhex(data_out)
        handshake_pair = data_in_bin, data_out_bin
    except ValueError:
        raise SystemExit(f'!!the passed {handshake_pair=} from `handshake` is corrupted, '
                         'check your configs and try again')
    return handshake_pair


def data_rows_guard(conf_value: str) -> Dict[bytes, List[bytes]]:
    """Check and transform the string data_rows value to the dict of responses in bytes"""
    data_rows = dict()
    for data_row in conf_value.splitlines():
        try:
            data_in, data_out = data_row.split(':')
            data_in_bin = bytes.fromhex(data_in)
            data_out_bin = list()
            for data_out_part in data_out.split(','):
                data_out_bin.append(bytes.fromhex(data_out_part))
        except ValueError:
            raise SystemExit(f'!!the passed {data_row=} from `data_rows` is corrupted, '
                             'check your configs and try again')
        data_rows[data_in_bin] = data_out_bin
    return data_rows


def allowed_hosts_guard(conf_value: str) -> List[str]:
    """Check and transform the string data_rows value to the list of strings one"""
    allowed_hosts = list()
    for host in conf_value.splitlines():
        try:
            inet_pton(AF_INET, host)
            allowed_hosts.append(host)
        except OSError:
            raise SystemExit('!!ip address must be a full IPv4 formatted string, '
                             f'passed value which triggered the error is {host}')
    return allowed_hosts


def get_configs(cfg_filename: str) -> Dict[str, Any]:
    assert isfile(cfg_filename), f'!!config with filename {cfg_filename} is not found'
    config_dict = dict()
    necessary_params = {
        'port': port_guard,
        'listen_address': listen_address_guard,
        'handshake': handshake_guard,
        'data_rows': data_rows_guard,
        'allowed_hosts': allowed_hosts_guard,
    }

    config = ConfigParser()
    config.read(cfg_filename)

    try:
        config_params = config[CFG_DEF_SECT]
    except KeyError:
        raise SystemError(f'!!section {CFG_DEF_SECT} was not found in {cfg_filename}')

    try:
        for param_name, param_guard in necessary_params.items():
            config_dict[param_name] = param_guard(config_params[param_name])
    except KeyError as ke:
        raise SystemError(f'!!necessary param {ke} in section {CFG_DEF_SECT} was not found in {cfg_filename}')

    return config_dict


if __name__ == '__main__':
    from pprint import pprint
    pprint(get_configs('test.ini'))
