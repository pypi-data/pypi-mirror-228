import logging
import pandas as pd
import subprocess
import os
import yaml
import json
import sys


"""#!/usr/bin/env python3

import json
import logging
import sys




if __name__ == '__main__':
    env = _parse_args(sys.argv)

    # Do your magic here
    raise NotImplementedError("TODO: implement the probe")
"""
# __root_dir__ = os.path.split(__file__)[0]
__install_dir__ = ''


def parse_cli(argv):
    try:
        return {'epath': argv[1], '_conf': json.loads(sys.argv[2])}
    except Exception:
        logging.exception("Unexpected error parsing arguments")


def list_probes():
    assert __install_dir__ not in ['', None], "__install_dir__ not specified"
    _prob_dir = os.path.join(__install_dir__, 'src', 'main', 'probe')
    _filtered = [os.path.abspath(i) for i in filter(
        lambda x: os.path.isfile(os.path.join(x, '.conf')) and os.path.isfile(os.path.join(x, 'main.py')),
        [os.path.join(_prob_dir, i) for i in next(os.walk(_prob_dir))[1]])]
    logging.debug(f"{len(_filtered)} probes found")
    return _filtered


def single_probe(probe_dir, target) -> list:
    """Prepares an environment to execute the probe

        Parses and validates the configuration file of the probe specified in the parameter, and the target file.
        Returns an object with all the information parsed. See :class:`ProbeEnvironment` for more information.

        :param probe_dir: dir name of the probe to be executed
        :param target:
        :return:
            Exit code (see Exit codes in the documentation for more info)
        """

    # def _probe_fullpath():
    #     return os.path.abspath(os.path.join(os.path.dirname(__file__), probe_dir, 'main.py'))

    # Parse conf file
    try:
        # __probe_dir__ = os.path.abspath(os.path.dirname(_probe_fullpath()))
        _probe_fullpath = os.path.abspath(os.path.join(probe_dir, 'main.py'))
        with open(os.path.join(os.path.dirname(_probe_fullpath), '.conf'), 'r') as conffile:
            _conf = yaml.safe_load(conffile)
            logging.debug(f"Probe initialized:{_conf}")
    except Exception:
        logging.exception("Unexpected error")
        exit(1)
        # raise error.FileNotFound
    # Execute the probe
    logging.info(f"Executing probe '{os.path.basename(probe_dir)}' on file {target}")
    returncode = subprocess.call(f"{_probe_fullpath} {target} '{json.dumps(_conf)}'", shell=True)

    # Return the result of the probe
    if returncode not in [0, 255]:
        logging.error(f"Probe '{probe_dir}' failed ({returncode})")
        return [_conf['id'], 901]
    else:
        logging.info(f"Probe completed ({returncode})")
        return [_conf['id'], returncode]


def multi_probe(probe_list: list, target) -> dict[pd.DataFrame]:
    # analyze_elf(elf_path=tg, test_battery=_final_tests, verbosity=args.v)
    # TODO: run all the corresponding probe
    # TODO: apply parallelism. The computations of each item are independent from the rest
    _results = []
    for probe in probe_list:
        _results.append(single_probe(probe, target))
    _df = pd.DataFrame(_results, columns=['probe_id', 'result'])
    logging.info(f"Analysis completed ({target}):\n{_df.to_string()}")
    return {target: _df}
