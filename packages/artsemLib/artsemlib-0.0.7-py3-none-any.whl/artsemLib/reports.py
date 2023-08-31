import subprocess
from hashlib import md5, sha1, sha256
import json
import logging
import os
import re

import pandas as pd

from collections import namedtuple

from tinydb import TinyDB, Query

ValidatedArgs = namedtuple('validatedArgs', ['source', 'report_name', 'template'])
ProbeSection = namedtuple('ProbeSection', ['info', 'result'])
__default_parser__ = 'txt'
__install_dir__ = ''


def get_parser_name(parser_path):
    return os.path.split(os.path.split(parser_path)[0])[1]


def default_template(parser_path):
    """Selects the first template in alphabetical order"""
    return sorted(list_templates(parser_path))[0]


def list_templates(parser_path):
    return list(
        map(lambda x: re.sub(f'\\.{get_parser_name(parser_path)}', '', x),
            filter(
                lambda x: os.path.splitext(x)[1][1:] == get_parser_name(parser_path),
                os.listdir(os.path.split(parser_path)[0]))))


def list_parsers():
    # https://stackoverflow.com/questions/141291/how-to-list-only-top-level-directories-in-python
    # iterate (absolute path) entries in this directory and filter by the sub-files included in it
    logging.info("Loading parsers")
    assert __install_dir__ not in ['', None], "__install_dir__ not specified"
    _parsers = [os.path.basename(x) for x in filter(
        lambda x: os.path.isfile(os.path.join(x, 'parser.py')) and f'.{os.path.basename(x)}' in '$'.join(
            os.listdir(x)),
        [os.path.join(__install_dir__, 'src', 'main', 'report', i)
         for i in next(os.walk(os.path.join(__install_dir__, 'src', 'main', 'report')))[1]])]
    logging.info(f"({len(_parsers)}) Parsers loaded: {[os.path.basename(x) for x in _parsers]}")


class AnalysisResult(dict):
    # https://stackoverflow.com/questions/2328235/pythonextend-the-dict-class
    headers = ['probe_id', 'result']

    # TODO: sort analysis results by ID
    def __init__(self, *args, **kwargs):
        super(AnalysisResult, self).__init__(*args, **kwargs)
        self.itemlist = super(AnalysisResult, self).keys()

    def add(self, subject, result: pd.DataFrame):
        self.update_state({subject: result})

    def update_state(self, *args, **kwargs):
        for arg in args:
            assert isinstance(arg, dict), f"Invalid type. Expected dict, obtained {type(arg)}"
            for k, v in arg.items():
                assert isinstance(k, str) and isinstance(v, pd.DataFrame), \
                    f"Invalid type. Expected string: pandas.DataFrame, obtained {type(k)}: {type(v)}"
        for k, v in kwargs:
            assert isinstance(k, str) and isinstance(v, pd.DataFrame), \
                f"Invalid type. Expected string: pandas.DataFrame, obtained {type(k)}: {type(v)}"
        self.update(*args, **kwargs)

    def __repr__(self):
        return '\n'.join([f"Showing analysis results\n"
                          f"FILE ANALYSIS: {k}\n{v.to_string()}\n{'-' * 25}" for k, v in self.items()])

    def to_json(self, path=None):
        if path is not None:
            with open(path, 'w', encoding='UTF-8') as outfile:
                json.dump({k: v.to_json() for k, v in self.items()}, outfile)
        return {k: v.to_json() for k, v in self.items()}

    @staticmethod
    def read_json(source):
        _ret = AnalysisResult()
        try:
            if os.path.isfile(source):
                logging.info(f"Parsing analysis results from file ({source})")
                with (open(source, 'r', encoding='UTF-8') as infile):
                    _ret.update_state(json.load(infile))
            else:
                logging.info(f"Parsing analysis results from input arguments")
                _ret.update_state(json.loads(source))
            logging.info("Analysis results parsed successfully")
        except json.decoder.JSONDecodeError:
            logging.exception("Unexpected error while parsing analysis results")
            exit(1)
        return _ret


class SubjectSection:

    def __init__(self, fpath):
        self.path = fpath
        # TODO: add hashes (md5, sha1, sha256) of each file to report
        try:
            with open(fpath, 'rb') as subjectfile:
                _fcontent = subjectfile.read()
                self.hash = {
                    'md5': md5(_fcontent).hexdigest(),
                    'sha1': sha1(_fcontent).hexdigest(),
                    'sha256': sha256(_fcontent).hexdigest()
                }
        except FileNotFoundError:
            logging.warning(f"The target file is not found ({fpath})")
            self.hash = {'md5': '', 'sha1': '', 'sha256': ''}
        self.probes = list()

    def add_probe_section(self, info: dict, result: int):
        # TODO: get prob by prob_id, and the result
        self.probes.append(ProbeSection(info, result))

    def __repr__(self):
        return str(self.__dict__)


class Report(list):
    def __init__(self, *args):
        # TODO: check and prompt to user if a file is going to be overwritten
        # self.contents = list()
        super(Report, self).__init__(*args)

    def add_subject_section(self, fpath):
        _s = SubjectSection(fpath)
        self.append(_s)
        return _s

    def load_results(self, results: AnalysisResult) -> None:
        """Load an :class:`AnalysisResult` object
        __db__.Probes table contains all the information of the probe
        results contains all the results of each probe for each file
        Combine them to generate a report:

        :param results: AnalysisResult object
        :return: None
        """

        logging.info("Loading analysis results")
        _db = TinyDB(os.path.join(__install_dir__, 'config', 'db.json'))
        for tg, probes in results.items():
            fsec = self.add_subject_section(tg)
            for index, row in pd.DataFrame(probes, columns=['probe_id', 'result']).iterrows():
                fsec.add_probe_section(
                    info=_db.table('Probes').search(Query().id == row['probe_id'])[0],
                    result=row['result'])
        logging.info("Analysis results loaded successfully. Report enriched")
        logging.debug(f"Enriched Report: {self.__dict__}")

    def write_to_file(self, fname, template=None) -> None:
        """Report derives the parser from file extension"""
        logging.info("Writing report to file")
        _parsername = os.path.splitext(str(fname))[1][1:]
        logging.debug(f"Attemp to use parser '{_parsername}'")
        if _parsername == '':
            _parsername = __default_parser__
        elif _parsername not in list_parsers():
            logging.error(f"Parser '{_parsername}' not found")
            logging.info(f"Failed to generate report ({fname})")
            return None
        else:
            # TODO import the corresponding parser class
            parser = os.path.join(os.path.dirname(__file__), _parsername, 'parser.py')
            a = f"-n {fname}" if fname is not None else ''
            b = f"-t {template}" if template is not None else ''
            returncode = subprocess.call(f"{parser} {a} {b}", shell=True)
            if returncode != 0:
                logging.error(f"Something went wrong generating the report ({fname})")
                return None
        # TODO: execute the corresponding formatter
        logging.info(f"Report generated successfully ({fname})")


def parse_cli(parser_path, cmd=None):
    import argparse
    parser = argparse.ArgumentParser(
        prog=f"{get_parser_name(parser_path)}_parser.py",
        description=f"Generate {get_parser_name(parser_path).upper()} reports from a given set of results")
    parser.add_argument(
        'source',
        type=str,
        help="AnalysisResult (JSON) object, in string format or a path to the file containing it")
    parser.add_argument(
        '-n', '--report-name',
        default='output',
        help="Name for the file. By default, 'output")
    parser.add_argument(
        '-t', '--template',
        default=None,
        choices=list_templates(parser_path),
        help="Template to be used for the report. "
             f"If not specified, the 1st template in alphabetical order ({default_template(parser_path)}) will be used")
    parser.add_argument(
        "-v",
        action="count",
        default=0,
        help="Increase logging verbosity [-v, -vv]")
    _args = parser.parse_args(cmd)
    if _args.v == 0:
        logging.basicConfig(level='WARN')
    elif _args.v == 1:
        logging.basicConfig(level='INFO')
    else:
        logging.basicConfig(level='DEBUG')
    logging.debug(f'CLI input args: {_args}')
    logging.debug("Validating input arguments")
    _valid = list()
    _parser_name = get_parser_name(parser_path)
    try:
        if os.path.isfile(_args.source):
            logging.info(f"Parsing analysis results from file ({_args.source})")
            with open(_args.source, 'r', encoding='UTF-8') as infile:
                _valid.append(json.load(infile))
        else:
            logging.info(f"Parsing analysis results from input arguments")
            _valid.append(json.loads(_args.source))
        logging.info("Analysis results parsed successfully")
    except json.decoder.JSONDecodeError:
        logging.exception("Unexpected error while parsing analysis results")
        exit(1)
    # Check whether source and template formatters match
    outfile_ext = os.path.splitext(_args.report_name)[1][1:]
    template_ext = os.path.splitext(_args.template)[1][1:] if _args.template is not None else ''
    if outfile_ext == '' or outfile_ext == _parser_name:
        logging.debug(f"File extension OK")
    else:
        logging.error(f"Invalid file extension ({outfile_ext}) for this parser ({_parser_name})")
        exit(2)
    if template_ext == '' or template_ext == _parser_name:
        logging.debug(f"Template extension OK")
    else:
        logging.error(f"Invalid template extension ({outfile_ext}) for this parser ({_parser_name})")
        exit(3)
    if '' not in [outfile_ext, template_ext] and outfile_ext != template_ext:
        logging.error(f"Output file extension and template extension do not match ({outfile_ext}/{template_ext})")
        exit(4)
    else:
        logging.debug("Output file extension and template extension match (OK)")
    _valid.append(_args.report_name)
    # Verify that the template specified in the arguments is included in the folder
    if _args.template is None:
        logging.info(f"Default template selected ({default_template(parser_path)})")
        _valid.append(default_template(parser_path))
    elif re.sub(f'\\.{get_parser_name(parser_path)}', '', _args.template) in list_templates(parser_path):
        logging.info(f"Template selected ({_args.template})")
        _valid.append(_args.template)
    else:
        logging.error(f"Template not found ({_args.template})")
        exit(5)
    _ret = ValidatedArgs(*_valid)
    logging.debug(f"Args validated successfully: {_ret}")
    return _ret

# if __name__ == '__main__':
#     # https://stackoverflow.com/questions/141291/how-to-list-only-top-level-directories-in-python
#     r = Report('a.md')
#     # print(next(os.walk('.'))[1])
#     # print(os.listdir(os.path.split(__file__)[0]))
