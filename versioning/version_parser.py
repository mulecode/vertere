import re

from versioning.version import Version
from versioning.version_tag_service import VersionTagParser


class InvalidVersionPrefixException(Exception):
    """Invalid version prefix"""
    pass


class InvalidSemanticVersionException(Exception):
    """Invalid semantic version"""
    pass


class VersionParser(object):
    def __init__(self, version_tag_parser: VersionTagParser):
        self.regex_prefix_only = r'^([a-zA-Z]+)$'
        self.regex_semantic = r'^([a-zA-Z]+)?((\d+)(\.)(\d+)(\.)(\d+))((\.)(\D+))?(\d+)?$'
        self.version_tag_parser = version_tag_parser

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
        return bool(pattern.match(str(value)))

    def parse(self, value: str) -> Version:
        if not self.is_version(value):
            raise InvalidSemanticVersionException(f'Value {value} is not a valid semantic version')

        pattern = re.compile(self.regex_semantic)
        search_result = pattern.search(str(value))

        prefix = search_result.group(1)
        major = search_result.group(3)
        minor = search_result.group(5)
        patch = search_result.group(7)
        tag_name = search_result.group(10)
        seq = search_result.group(11)

        # print(f'parsed: {prefix} {major} {minor} {patch} {tag_name} {seq}')

        parsed_version = Version()
        parsed_version.prefix = prefix if prefix else ''
        parsed_version.major = int(major)
        parsed_version.minor = int(minor)
        parsed_version.patch = int(patch)

        if tag_name:
            parsed_tag = self.version_tag_parser.parse_tag(tag_name, seq)
            parsed_version.tag = parsed_tag

        return parsed_version

    def get_version_tag_parser(self) -> VersionTagParser:
        return self.version_tag_parser
