from os.path import isfile
from typing import Union, Dict, List
from configparser import ConfigParser

CFG_DEF_SECT = 'main'


def get_configs(cfg_filename: str) -> Dict[str, Union[int, str, List[str]]]:
    assert isfile(cfg_filename), f'!!config with filename {cfg_filename} is not found'
    config_dict = dict()
    # TODO: guard the transformation functions (ex. if `port` is "some text")
    #       + check parameter syntax (ex `ip` is "d.d.d.d", not something else)
    necessary_params = {
        'port': int,
        'listen_address': str,
        'data_rows': lambda s: map(str.encode, s.split('\n')),
        'allowed_hosts': lambda s: s.split('\n'),
    }

    config = ConfigParser()
    config.read(cfg_filename)

    try:
        config_params = config[CFG_DEF_SECT]
    except KeyError:
        print(f'!!section {CFG_DEF_SECT} was not found in {cfg_filename}')
        return {}

    try:
        for param_name, param_translator in necessary_params.items():
            config_dict[param_name] = param_translator(config_params[param_name])
    except KeyError as ke:
        print(f'!!necessary param {ke} in section {CFG_DEF_SECT} was not found in {cfg_filename}')
        return {}
    except Exception as e:
        print(f'!!some unexpected error happened, details: {e}')

    return config_dict


if __name__ == '__main__':
    from pprint import pprint
    pprint(get_configs('test.ini'))
