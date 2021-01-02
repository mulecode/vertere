import json
from pkg_resources import Requirement, resource_filename

from versioning.version_tag import VersionPostfix


class VersionPostfixLoader(object):
    def __init__(self):
        self.postfix_config_location = 'data/postfix_config.json'
        self.loaded_postfixes_data = []
        self.__load_postfix_configuration__()

    def __load_postfix_configuration__(self):
        filename = resource_filename(Requirement.parse("versioning"), self.postfix_config_location)
        with open(filename) as json_file:
            self.loaded_postfixes_data = json.load(json_file)

    def get_all_postfix_configuration(self):
        return self.loaded_postfixes_data


class VersionPostfixParser(object):
    def __init__(self, version_postfix_loader: VersionPostfixLoader):
        self.version_postfix_loader = version_postfix_loader
        self.configured_postfixes = []
        self.__load_configured_postfixes__()

    def __load_configured_postfixes__(self):
        postfix_list = []
        data = self.version_postfix_loader.get_all_postfix_configuration()
        for p in data:
            config_parsed = self.__parse_postfix_config__(p)
            postfix_list.append(config_parsed)
        self.configured_postfixes = postfix_list

    def __parse_postfix_config__(self, value) -> 'PostfixConfig':
        postfix_config = PostfixConfig()
        postfix_config.name = value['name']
        postfix_config.weight = int(value['weight'])
        postfix_config.with_seq = bool(value['with_seq'])
        postfix_config.promotable = bool(value['promotable'])
        return postfix_config

    def validate_postfix_name(self, postfix_name: str):
        if not postfix_name:
            return
        if not self.find_postfix_config_by_name(postfix_name):
            raise InvalidVersionPostfixException(
                f'Unpassable postfix {postfix_name}. available options: [{self.get_postfixes_joined()}]'
            )

    def find_postfix_config_by_name(self, postfix_name) -> 'PostfixConfig':
        return next(
            filter(
                lambda t: t.name == postfix_name, self.configured_postfixes
            ), None)

    def get_postfixes_joined(self) -> str:
        postfix_list = map(lambda t: t.name, self.configured_postfixes)
        return ', '.join(postfix_list)

    def count(self) -> int:
        return len(list(self.configured_postfixes))

    def parse_postfix(self, postfix_name, seq) -> VersionPostfix:
        postfix_config = self.find_postfix_config_by_name(postfix_name)

        if not postfix_config:
            raise InvalidVersionPostfixException(
                f'Could not parse - Invalid postfix {postfix_name}, available options: [{self.get_postfixes_joined()}]'
            )

        if postfix_config.with_seq and seq is None:
            raise InvalidVersionPostfixException(
                f'Could not parse - Postfix {postfix_name} is set with no sequencer. Found sequencer set to {seq}'
            )

        if postfix_config.with_seq and (seq is not None and int(seq) <= 0):
            raise InvalidVersionPostfixException(
                f'Could not parse - Postfix sequencer should be bigger than 0. Found {seq}'
            )

        if not postfix_config.with_seq and seq is not None:
            raise InvalidVersionPostfixException(
                f'Could not parse - Postfix {postfix_name} is set with no sequencer, but found sequencer equals to {seq}'
            )

        parsed_postfix = VersionPostfix()
        parsed_postfix.name = postfix_name
        parsed_postfix.weight = int(postfix_config.weight) if postfix_config.weight else 0
        parsed_postfix.seq = int(seq) if seq else None

        return parsed_postfix


class InvalidVersionPostfixException(Exception):
    """Invalid version postfix"""
    pass


class PostfixConfig(object):
    def __init__(self):
        self.name = ''
        self.weight = 1
        self.with_seq = False
        self.promotable = False

    def __str__(self):
        return f'<name: {self.name}, ' \
               f'weight: {self.weight}, ' \
               f'with_seq: {self.with_seq}, ' \
               f'promotable: {self.promotable}>'
