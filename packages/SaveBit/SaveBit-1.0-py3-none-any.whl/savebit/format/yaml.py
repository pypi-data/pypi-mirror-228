import yaml
from ..env import *


class main:
    def __init__(self, file_path: str, info):
        self.file_path = file_path
        self.data = self._read()

    def _read(self):
        self.data = yaml.load(open(self.file_path, "r"))

    def _reload(self):
        self._read()

    def write(self, data: object):
        if get_data_type(data) not in format_data["yaml"]["type"]:
            raise Exception("data type is not yaml")
        else:
            yaml.dump(data, open(self.file_path, "w"))
        self._reload()

    def clean(self):
        self.write({})


def creater(file_path):
    data = "{}"
    f = open(file_path, "w")
    f.write(data)
    f.close()
