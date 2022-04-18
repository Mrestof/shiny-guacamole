from configparser import ConfigParser

CFG_FILENAME = 'config.ini'


def get_configs(section: str) -> dict[str, int | str | list[str]]:
    config_dict = dict()
    necessary_params = {
        'port': int,
        'listen_address': str,
        'data_rows': lambda s: map(str.encode, s.split('\n')),
        'allowed_hosts': lambda s: s.split('\n'),
    }

    config = ConfigParser()
    config.read(CFG_FILENAME)

    try:
        config_params = config[section]
    except KeyError:
        print(f'!!section {section} was not found in {CFG_FILENAME}')
        return {}

    try:
        for param_name, param_translator in necessary_params.items():
            config_dict[param_name] = param_translator(config_params[param_name])
    except KeyError as ke:
        print(f'!!necessary param {ke} in section {section} was not found in {CFG_FILENAME}')
        return {}
    except Exception as e:
        print(f'!!some unexpected error happened, details: {e}')

    return config_dict


if __name__ == '__main__':
    print(get_configs('test'))
