class VersionStorage(object):
    def __init__(self):
        self.output_file_name = '.versioning_out.txt'

    def persist(self, value: str):
        with open(self.output_file_name, "w") as f:
            f.write(value)

    def read(self) -> str:
        with open(self.output_file_name, "r") as f:
            return f.readline().rstrip()
