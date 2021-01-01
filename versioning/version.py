from versioning.incrementer import Incrementer
from versioning.version_tag import VersionTag


def justify(value):
    return str(value).rjust(5, '0')


class Version(object):
    prefix = ''
    major = 1
    minor = 0
    patch = 0
    tag: VersionTag = None

    def to_hash(self):
        if not self.tag:
            return (
                    justify(self.major) +
                    justify(self.minor) +
                    justify(self.patch) +
                    '99999' +
                    '99999'
            )
        return (
                justify(self.major) +
                justify(self.minor) +
                justify(self.patch) +
                justify(self.tag.weight) +
                justify(self.tag.seq)
        )

    def __str__(self):
        base_str = f'{self.prefix}{self.major}.{self.minor}.{self.patch}'
        if self.tag:
            return f'{base_str}.{self.tag}'
        return base_str

    # def reset_version_seq(self):
    #     self.seq = 1

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
