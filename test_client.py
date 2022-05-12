# TODO: cover the code with exceptions
# TODO: add command line parameters:
#       - list of tests to accomplish
# TODO: add command line prompt to execute tests in interactive way
from sys import argv
from typing import List
from dataclasses import dataclass
from testing.tests import *
from cfg.loader import get_configs


@dataclass(init=False)
class TCArgs:
    config_filename: str
    config_required_test_names: List[str]


def get_args() -> TCArgs:
    args = TCArgs()
    try:
        args.config_filename = argv[1]
    except IndexError:
        raise SystemExit(f'!!usage: {argv[0]!r} config_name.ini [test_functions_to_run_separated_by_space]')
    args.config_required_test_names = argv[2:]
    return args


def main() -> None:
    available_tests = full,  # it is a tuple
    name_to_test_map = {test.__name__: test for test in available_tests}
    args = get_args()
    config = get_configs(args.config_filename)
    print(f'##start running tests, amount of tests: {len(test_names := args.config_required_test_names)}')
    try:
        for test_name in test_names:
            name_to_test_map[test_name](config)  # can only test on locally run server
    except KeyError as ke:
        raise SystemExit(f'!!test named {ke} is not found in {args.config_filename!r} config')
    print('##finish all tests')


if __name__ == '__main__':
    main()
