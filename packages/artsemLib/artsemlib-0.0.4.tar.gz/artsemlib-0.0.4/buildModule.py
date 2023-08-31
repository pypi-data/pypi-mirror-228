import logging
import os
import subprocess
import sys
from re import fullmatch

__interpreter__ = 'python3' if sys.platform.find('linux') != -1 else 'python.exe'
__build_tools__ = ['twine', 'build']


def parse_args(cmd=None):
    import argparse
    parser = argparse.ArgumentParser(
        prog=os.path.basename(__file__),
        description="Builds and publish artsemLib package")
    parser.add_argument(
        "-v",
        action="count",
        default=0,
        help="increase logging verbosity [-v, -vv]")
    parser.add_argument(
        "-p", "--publish",
        nargs='*',
        type=str,
        metavar="NEW_VERSION",
        help="If build success, publish the NEW_VERSION package to the repository"
    )
    parser.add_argument(
        "-V", "--version",
        action="store_true",
        default=False,
        help="Print the current package version and exits"
    )
    _a = parser.parse_args(cmd)
    if _a.v == 0:
        logging.basicConfig(level='WARN')
    elif _a.v == 1:
        logging.basicConfig(level='INFO')
    else:
        logging.basicConfig(level='DEBUG')
    logging.debug(f"CLI arguments: {_a}")
    return _a


def auto_increment_version(v) -> str:
    _version = str(v).split('.')
    _version[-1] = str(int(_version[-1]) + 1)
    logging.info(f"Auto incrementing version ({v} -> {'.'.join(_version)})")
    return '.'.join(_version)


def get_current_version() -> str:
    _result = subprocess.run([__interpreter__, '-m', 'hatch', 'version'], stdout=subprocess.PIPE)
    return _result.stdout.decode('utf-8').replace('\n', '').strip()


def run_cmd(cmd):
    _ret = os.system(f"{cmd}")
    logging.debug(f"Command completed: {cmd} -> {_ret}")
    return _ret


def validate_version(version) -> bool:
    """Validates the syntax of a version number

    :param version: version number to be validated
    :return: True if version is valid
    """
    return fullmatch('(\\d+\\.)*\\d+', version) is not None


if __name__ == '__main__':
    _args = parse_args()
    if _args.publish is not None and len(_args.publish) > 1:
        logging.error(f"More than one version specified. Please use only one version at a time")
        exit(1)

    if _args.version:
        print(f"Current package version: {get_current_version()}")
        exit(0)
    # TODO: continue with the build process only if the previous command executed successfully
    logging.info(f"Updating build tools {__build_tools__}...")
    run_cmd(f'{__interpreter__} -m pip install --upgrade {" ".join(__build_tools__)}')
    os.chdir(os.path.dirname(__file__))
    logging.info(f"Building module...")
    run_cmd(f'{__interpreter__} -m build')
    logging.info(f"Build completed successfully")
    if _args.publish is not None:
        if len(_args.publish) == 0:
            _new_v = auto_increment_version(get_current_version())
        else:
            _new_v = _args.publish[0]
            logging.info(f"Manual versioning ({get_current_version()} -> {_new_v})")
        if validate_version(_new_v):
            run_cmd(f"{__interpreter__} -m hatch version {_new_v}")
            logging.info(f"Publishing package...")
            run_cmd(f"{__interpreter__} -m hatch publish")
            logging.info(f"Package published successfully")
        else:
            logging.error(f"Invalid syntax version ({_new_v}). Allowed [x.]x, where x are integers")
            logging.error("Publishing process aborted")
    logging.info("Execution completed. Exiting...")
    exit(0)
