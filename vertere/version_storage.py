from os import path


class VersionStorage(object):
    def __init__(self):
        self.output_file_name = '.vertere_out.txt'

    def persist(self, value: str):
        with open(self.output_file_name, "w") as f:
            f.write(value)

    def read(self) -> str:
        exists = path.exists(self.output_file_name)
        if not exists:
            raise FileNotFoundException(f'Cannot read content of file {self.output_file_name} - File does not exists')
        with open(self.output_file_name, "r") as f:
            return f.readline().rstrip()


class FileNotFoundException(Exception):
    pass
