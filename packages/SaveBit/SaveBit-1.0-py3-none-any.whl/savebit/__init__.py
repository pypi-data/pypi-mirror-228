from .format import *
import os
from .env import *


class Savebit:
    def __init__(self, save_type: str = "txt", dir: str = ".", suffix: str = ".dat"):
        if save_type not in [
            "pickle",
            "json",
            "yaml",
            "ini",
        ]:
            raise TypeError("save_type must be 'txt' or 'pkl'")
        self.type = save_type
        print(self.type)
        self.dir = dir
        self.suffix = suffix

    # 新建
    def creater(self, name: str):
        if "/" in name or "\\" in name:
            raise TypeError("name can't contain '/' or '\\'")
        file_path = os.path.join(self.dir, name + self.suffix)
        clas = getattr(format, self.type)
        clas.creater(file_path)
        print(clas)
        data_type = clas.main(file_path, self)
        return data_type
