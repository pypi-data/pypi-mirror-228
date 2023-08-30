#!/usr/bin/env python3
import sys
import traceback

from fovus.cli.cli_action_runner import CliActionRunner
from fovus.cli.fovus_cli_argument_parser import FovusCliArgumentParser

OK_RETURN_STATUS = 0
ERROR_RETURN_STATUS = 1


def main():
    return_status = OK_RETURN_STATUS
    debug = False
    if "--debug" in sys.argv:
        debug = True
        sys.argv.remove("--debug")
    try:
        _main()
    except Exception as exception:  # pylint: disable=broad-except
        if debug:
            print(traceback.format_exc())
        else:
            print(exception)
        return_status = ERROR_RETURN_STATUS
    finally:
        return return_status  # pylint: disable=lost-exception


def _main():
    parser = FovusCliArgumentParser()
    parser.parse_args()
    parser.merge_args_with_config()
    parser.update_overridden_configs()
    cli_action_runner = CliActionRunner(parser.get_args_dict())
    cli_action_runner.run_actions()


if __name__ == "__main__":
    sys.exit(main())
