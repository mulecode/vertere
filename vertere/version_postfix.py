class VersionPostfix(object):
    name: str = None
    weight: int = None
    seq: int = None

    def __str__(self):
        if self.seq:
            return f'{self.name}{self.seq}'
        return f'{self.name}'

    def reset_seq(self):
        self.seq = None

    def increase_seq(self):
        if not self.seq:
            self.seq = 1
            return
        self.seq += 1
