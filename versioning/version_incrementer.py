from enum import Enum


class Incrementer(Enum):
    PATCH = 1
    MINOR = 2
    MAJOR = 3

    def __str__(self):
        return self.name


class IncrementerParser(object):
    def __init__(self):
        pass

    def parse(self, value: str) -> Incrementer:
        if not value:
            return None
        try:
            return Incrementer[value.strip().upper()]
        except Exception:
            raise InvalidIncrementTypeException()


class InvalidIncrementTypeException(Exception):
    """Invalid Incrementer type"""
    pass
