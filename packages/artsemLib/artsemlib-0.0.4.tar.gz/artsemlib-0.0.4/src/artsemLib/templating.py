import logging
import os.path
import re

__default_replacement__ = ''


class Template:
    def __init__(self, name: str, stencil: str):
        self.name = name
        self.stencil = str(stencil)

    @property
    def length(self):
        return len(self.stencil)

    def __repr__(self):
        return str(self.__dict__)

    def list_replacements(self) -> list:
        return list(set(re.findall('&\\w*&', self.stencil)))

    def fill(self, **kwargs) -> str:
        _ret = str(self.stencil)
        logging.info(f"Filling {'static' if len(self.list_replacements()) == 0 else 'dynamic'} template ({self.name})")
        logging.debug(f"Fill input arguments: {kwargs}")
        # Iterate all unique replacing variables
        for r in self.list_replacements():
            if r[1:-1] in kwargs:
                replacement = str(kwargs.get(r[1:-1]))
            else:
                logging.warning(f"Missing template parameter ({r[1:-1]}). Default value will be used")
                replacement = __default_replacement__
            _ret = _ret.replace(r, replacement)
        logging.info(f"Template filled successfully")
        return _ret


class TemplateBook:
    def __init__(self, title):
        self.title = title
        self.templates = list()

    def __repr__(self):
        return str(self.__dict__)

    def list_templates(self) -> list:
        return [t.name for t in self.templates]

    def add_tmpt(self, name, stencil):
        self.templates.append(Template(name, stencil))

    def fill_tmpt(self, tname, **kwargs) -> str | None:
        _t = None
        for i in self.templates:
            if i.name == tname:
                _t = i
                break
        if _t is None:
            logging.error(f"Template not found ({tname})")
            return None
        else:
            return _t.fill(**kwargs)

    @staticmethod
    def load_tmpt(fpath):
        assert os.path.splitext(fpath)[1] == '.tmpt', \
            f"Invalid file extension. Expected .tmpt, obtained {os.path.splitext(fpath)[1]}"
        try:
            logging.info(f"Loading Template Book from file ({fpath})")
            _ret = TemplateBook(os.path.splitext(os.path.basename(fpath))[0])
            with open(fpath, 'r', encoding='utf-8') as tmptfile:
                # Join all lines, split by special character '&&&' and '&'
                for t in [x.split('\n%\n') for x in ''.join(tmptfile.readlines()).split('\n%%%\n')]:
                    _ret.add_tmpt(*t)
            logging.info(f"{len(_ret.templates)} Templates loaded: {_ret.list_templates()}")
            return _ret
        except Exception:
            logging.exception(f"Unexpected error parsing template book ({fpath})")
            return None


if __name__ == '__main__':
    logging.basicConfig(level='DEBUG')
    tb = TemplateBook.load_tmpt(
        '/home/redwing/PycharmProjects/artsem/src/main/module/artsem/src/artsem/templates/exitcode.tmpt')

    print(tb.fill_tmpt(tname='ErrorClass', errdesc="Just some descriptions", errid="100", errlabel="TooBigToMyLittle"))
    print(tb.fill_tmpt(tname='Header', errdesc="Just some descriptions", errid="100", errlabel="TooBigToMyLittle"))

