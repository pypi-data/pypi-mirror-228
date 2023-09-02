import configparser


class main:
    def __init__(self, file_path: str, info):
        self.file_path = file_path
        self.data = self._read()

    def _recursive_dict_iteration(self, dictionary):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                self._recursive_dict_iteration(value)
            else:
                print(f"Key: {key}, Value: {value}")

    def _read(self):
        config = configparser.ConfigParser()
        config.read(self.file_path)
        self.data = config
        return config

    def write(self, section, *args, **kwargs):
        self.data.set(section, *args, **kwargs)
        with open(self.file_path, "w") as configfile:
            self.data.write(configfile)


def creater(file_path):
    f = open(file_path, "w")
    f.close()
