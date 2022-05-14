# TODO: cover the code with exceptions
# TODO: add command line prompt to execute tests in interactive way
from sys import argv
from time import sleep
from typing import List
from dataclasses import dataclass
from server import Args
from testing.tests import *
from cfg.loader import get_configs


@dataclass
class TCArgs(Args):
    config_filename: str
    config_required_test_names: List[str]


def get_args() -> TCArgs:
    usage = (f'!!usage: {argv[0]!r} <config_name.ini> [test_functions_to_run_separated_by_space]',
             '\t<config_name.ini>: full or relative path to the configuration file in dosini format\n'
             '\t[test_functions_to_run_separated_by_space]: name(s) of test functions to run as separate arguments,'
             ' repeating is allowed (ex. full part full full)')
    try:
        if argv[1] == '--help':
            print('\n'.join(usage))
            raise SystemExit(0)
        config_filename = argv[1]
        config = get_configs(config_filename)
    except IndexError:
        raise SystemExit(usage[0])
    config_required_test_names = argv[2:]
    return TCArgs(config, config_filename, config_required_test_names)


def main() -> None:
    available_tests = full,  # it is a tuple
    name_to_test_map = {test.__name__: test for test in available_tests}
    args = get_args()
    print(f'##start running tests, amount of tests: {len(args.config_required_test_names)}')
    try:
        for test_name in args.config_required_test_names:
            name_to_test_map[test_name](args.config)  # can only test on locally run server
            # Q: clumsy crutch (or is it?) because if there is no pause between tests, the client crashes
            # to reproduce: `test_client <cfg> full full` without `sleep` below
            sleep(0.1)
    except KeyError as ke:
        raise SystemExit(f'!!test named {ke} is not found in {args.config_filename!r} config')
    print('##finish all tests')


if __name__ == '__main__':
    main()
