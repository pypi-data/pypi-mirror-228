import pickle


class main:
    def __init__(self, file_path: str, info):
        self.file_path = file_path
        self.data = self._read()
        self.info = info

    def _reload(self):
        self.data = self._read()
        return self.data

    def _read(self):
        self.data = pickle.load(open(self.file_path, "rb"))
        return self.data

    def write(self, data: object):
        data = pickle.dumps(data)
        f = open(self.file_path, "wb")
        f.write(data)
        f.close()
        self._reload()

    def clean(self):
        self.write("")
        self._reload()


def creater(file_path):
    data = pickle.dumps("")
    f = open(file_path, "wb")
    f.write(data)
