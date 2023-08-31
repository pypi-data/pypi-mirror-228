import logging
import os
import artsemLib


class ExitCode:
    _id_regex = '^[0-9]+[0-9]*$'
    _label_regex = '^[a-zA-Z0-9]*$'
    _range = range(0, 256)

    def __init__(self, excode, label, desc):
        import re
        self.id = int(excode)
        self.label = label
        self.desc = desc

        # Validate the values
        if re.fullmatch(ExitCode._id_regex, str(self.id)) is None or self.id not in ExitCode._range:
            raise SyntaxError(f'Invalid identifier ({excode}). Allowed [{ExitCode._range[0]}, {ExitCode._range[-1]}]')
        if re.fullmatch(ExitCode._label_regex, label) is None:
            raise SyntaxError(f'Invalid label ({label}). Use only alpha-numeric characters and camel case')
        if self.desc in ['', None]:
            logging.warning(f"Empty description for Exit Code '{self.id}')")

    def to_python_code(self) -> str:
        template_book = artsemLib.TemplateBook.load_tmpt(
            os.path.join(os.path.dirname(__file__), 'templates', 'exitcode.tmpt'))
        return template_book.fill_tmpt("ErrorClass", errid=self.id, errlabel=self.label, errdesc=self.desc)

    def __str__(self):
        return f"{self.id}-{self.label}:{self.desc}"


def compile_exitcodes(csv_path, outfile=None):
    """Generates the python file with all error classes

    Parses the file conf/exitcodes.csv, validating the input values.
    If the input file is valid, a python file which contains all error classes is generated.
    For more information check 'Error Codes' documentation.

    :return: None
    """
    import csv

    template_book = artsemLib.TemplateBook.load_tmpt(
        os.path.join(os.path.dirname(__file__), 'templates', 'exitcode.tmpt'))

    logging.info("Compiling Exit Codes")

    with open(csv_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')  # id, label, desc
        _unique_labels = []
        _unique_ids = []
        _all_exitcodes = []
        lcount = 1  # Line 0 is the header
        for row in reader:
            lcount += 1
            try:
                err = ExitCode(row['id'].strip(), row['label'].strip(), row['desc'].strip())
            except AttributeError:
                raise AttributeError(f'Missing attribute (exitcodes.csv:{lcount})')
            except SyntaxError:
                logging.exception(f"Syntax error (exitcodes.csv:{lcount})")
            # Avoid duplicates
            if err.id in _unique_ids:
                raise KeyError(f'Duplicated Exit code ID (exitcodes.csv:{lcount})')
            else:
                _unique_ids.append(err.id)
            if err.label in _unique_labels:
                raise KeyError(f'Duplicated label (exitcodes.csv:{lcount})')
            else:
                _unique_labels.append(err.label)
            _all_exitcodes.append(err)  # If all checks completed successfully
    logging.info(f'{len(_all_exitcodes)} Exit Codes compiled successfully')

    logging.info(f"Generating exit codes class file")
    if outfile is None:
        outfile = os.path.join(os.path.dirname(csv_path), 'error.py')
    with open(outfile, 'w', encoding='utf-8') as errfile:
        errfile.write(template_book.fill_tmpt('ExitCodeClassHeader'))
        # Generate all the Error classes iterating all ExitCode objects
        errfile.write('\n\n\n'.join([err.to_python_code() for err in _all_exitcodes]) + '\n')
    logging.info(f"Error class file generated successfully ({outfile})")
    return _all_exitcodes


def exitcodes_cli(cmd=None):
    """
    exitcodes compile /path/to/csv -> generate class file and return json object
    :param cmd: Command line arguments (list format)
    :return:
    """
    import argparse
    parser = argparse.ArgumentParser(
        prog=os.path.basename(__file__),
        description="Compile Exit Codes from CSV file and generate the corresponding Error class file"
    )
    parser.add_argument(
        'srcfile',
        metavar="FILE_CSV",
        help="Path to the CSV file with the Exit code details"
    )
    parser.add_argument(
        "-O", "--output",
        default=None,
        help="Path of the output file ('./error.py' by default)")
    parser.add_argument(
        "-v",
        action="count",
        default=0,
        help="increase logging verbosity [-v, -vv]")
    _a = parser.parse_args(cmd)
    if _a.v == 0:
        logging.basicConfig(level='WARN')
    elif _a.v == 1:
        logging.basicConfig(level='INFO')
    else:
        logging.basicConfig(level='DEBUG')
    logging.debug(f"CLI arguments: {_a}")
    return _a


if __name__ == '__main__':
    args = exitcodes_cli()
    compile_exitcodes(args.srcfile, args.output)
    exit(0)
