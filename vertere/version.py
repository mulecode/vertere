from vertere.incrementer import Incrementer
from vertere.version_postfix import VersionPostfix


class Version(object):
    prefix = ''
    major = 1
    minor = 0
    patch = 0
    postfix: VersionPostfix = None

    def to_hash(self):
        if not self.postfix:
            return (
                    self.__hash_justify__(self.major) +
                    self.__hash_justify__(self.minor) +
                    self.__hash_justify__(self.patch) +
                    '99999' +
                    '99999'
            )
        return (
                self.__hash_justify__(self.major) +
                self.__hash_justify__(self.minor) +
                self.__hash_justify__(self.patch) +
                self.__hash_justify__(self.postfix.weight) +
                self.__hash_justify__(self.postfix.seq)
        )

    def __hash_justify__(self, value):
        return str(value).rjust(5, '0')

    def __str__(self):
        base_str = f'{self.prefix}{self.major}.{self.minor}.{self.patch}'
        if self.postfix:
            return f'{base_str}.{self.postfix}'
        return base_str

    def increment_version(self, incrementer: Incrementer):
        if incrementer == Incrementer.PATCH:
            self.patch += 1
        if incrementer == Incrementer.MINOR:
            self.patch = 0
            self.minor += 1
        if incrementer == Incrementer.MAJOR:
            self.patch = 0
            self.minor = 0
            self.major += 1
