import json
from pkg_resources import Requirement, resource_filename

from versioning.version_tag import VersionTag


class VersionTagLoader(object):
    def __init__(self):
        self.tag_config_location = 'data/tag_config.json'
        self.loaded_tags_data = []
        self.__load_tags_configuration__()

    def __load_tags_configuration__(self):
        filename = resource_filename(Requirement.parse("versioning"), self.tag_config_location)
        print(f'load_configured_tags: {filename}')
        with open(filename) as json_file:
            self.loaded_tags_data = json.load(json_file)

    def get_tags_configuration(self):
        return self.loaded_tags_data


class VersionTagParser(object):
    def __init__(self, version_tag_loader: VersionTagLoader):
        self.tag_config_location = 'data/tag_config.json'
        self.version_tag_loader = version_tag_loader
        self.configured_tags = []
        self.__load_configured_tags__()

    def __load_configured_tags__(self):
        tag_list = []
        data = self.version_tag_loader.get_tags_configuration()
        for p in data:
            config_parsed = self.__parse_tag_config__(p)
            tag_list.append(config_parsed)
        self.configured_tags = tag_list

    def __parse_tag_config__(self, value) -> 'TagConfig':
        tag_config = TagConfig()
        tag_config.name = value['name']
        tag_config.weight = int(value['weight'])
        tag_config.with_seq = bool(value['with_seq'])
        tag_config.promotable = bool(value['promotable'])
        return tag_config

    def validate_tag_name(self, tag_name: str):
        if not tag_name:
            return
        if not self.find_config_by_tag_name(tag_name):
            raise InvalidSemanticTagVersionException(
                f'Unpassable tag {tag_name}. available options: [{self.available_tags()}]'
            )

    def find_config_by_tag_name(self, tag_name) -> 'TagConfig':
        return next(
            filter(
                lambda t: t.name == tag_name, self.configured_tags
            ), None)

    def available_tags(self) -> str:
        available_tags = map(lambda t: t.name, self.configured_tags)
        return ', '.join(available_tags)

    def count(self) -> int:
        return len(list(self.configured_tags))

    def parse_tag(self, tag_name, seq) -> VersionTag:
        tag_config = self.find_config_by_tag_name(tag_name)

        if not tag_config:
            raise InvalidSemanticTagVersionException(
                f'Could not parse - invalid tag {tag_name}, available options: [{self.available_tags()}]'
            )

        if tag_config.with_seq and seq is None:
            raise InvalidSemanticTagVersionException(
                f'Could not parse - Tag {tag_name} is set with no sequencer. Found sequencer set to {seq}'
            )

        if tag_config.with_seq and (seq is not None and int(seq) <= 0):
            raise InvalidSemanticTagVersionException(
                f'Could not parse - Tag sequencer should be bigger than 0. Found {seq}'
            )

        #  TODO review this case:
        if not tag_config.with_seq and seq is not None:
            raise InvalidSemanticTagVersionException(
                f'Could not parse - Tag {tag_name} is set with no sequencer, but found sequencer equals to {seq}'
            )

        parsed_tag = VersionTag()
        parsed_tag.name = tag_name
        parsed_tag.weight = tag_config.weight
        parsed_tag.seq = seq

        return parsed_tag


class InvalidSemanticTagVersionException(Exception):
    """Invalid tag semantic version"""
    pass


class TagConfig(object):
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
