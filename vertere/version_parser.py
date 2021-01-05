import re

from vertere.version import Version
from vertere.version_postfix_parser import VersionPostfixParser


class InvalidVersionPrefixException(Exception):
    """Invalid version prefix"""
    pass


class InvalidSemanticVersionException(Exception):
    """Invalid semantic version"""
    pass


class VersionParser(object):
    def __init__(self, version_postfix_parser: VersionPostfixParser):
        self.regex_prefix_only = r'^([a-zA-Z]+)$'
        self.regex_semantic = r'^([a-zA-Z]+)?((\d+)(\.)(\d+)(\.)(\d+))((\.)(\D+))?(\d+)?$'
        self.version_postfix_parser = version_postfix_parser

    def validate_version(self, value):
        if not value:
            return
        try:
            self.parse(value)
        except Exception as e:
            raise InvalidSemanticVersionException(f'Value {value} is not a valid semantic version - {e}')

    def validate_prefix(self, value):
        if not value:
            return
        pattern = re.compile(self.regex_prefix_only)
        if not bool(pattern.match(str(value))):
            raise InvalidVersionPrefixException(f'Invalid Version prefix value: {value}')

    def is_version(self, value: str):
        pattern = re.compile(self.regex_semantic)
        if not bool(pattern.match(str(value))):
            return False
        search_result = pattern.search(str(value))
        postfix_name = search_result.group(10)
        seq = search_result.group(11)
        if postfix_name:
            return self.version_postfix_parser.is_valid(postfix_name, seq)
        return True

    def parse(self, value: str) -> Version:
        if not self.is_version(value):
            raise InvalidSemanticVersionException(f'Value {value} is not a valid semantic version')

        pattern = re.compile(self.regex_semantic)
        search_result = pattern.search(str(value))

        prefix = search_result.group(1)
        major = search_result.group(3)
        minor = search_result.group(5)
        patch = search_result.group(7)
        postfix_name = search_result.group(10)
        seq = search_result.group(11)

        parsed_version = Version()
        parsed_version.prefix = prefix if prefix else ''
        parsed_version.major = int(major)
        parsed_version.minor = int(minor)
        parsed_version.patch = int(patch)

        if postfix_name:
            parsed_postfix = self.version_postfix_parser.parse_postfix(postfix_name, seq)
            parsed_version.postfix = parsed_postfix

        return parsed_version

    def get_version_postfix_parser(self) -> VersionPostfixParser:
        return self.version_postfix_parser
