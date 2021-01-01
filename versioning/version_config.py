import yaml
from os import path

from versioning.version_incrementer import Incrementer, IncrementerParser
from versioning.version_parser import VersionParser
from versioning.version_tag_service import TagConfig, VersionTagParser


class PromoterConfigLoader(object):
    config_file_name = 'versioning.yml'

    def __init__(self, version_parser: VersionParser,
                 version_tag_parser: VersionTagParser,
                 incrementer_parser: IncrementerParser):
        self.version_parser = version_parser
        self.version_tag_parser = version_tag_parser
        self.incrementer_parser = incrementer_parser

    def validate_config_path(self, config_path: str):
        if not config_path:
            return
        config_exists = path.exists(config_path)
        if not config_exists:
            raise LoadConfigFileException(f'Error loading config file {config_path} - File does not exists')

    def load_config_from_file(self, config_path: str = config_file_name) -> 'VersionConfig':

        default_config = VersionConfig()

        config_exists = path.exists(config_path)
        if not config_exists:
            return default_config

        config = yaml.safe_load(open(config_path))
        print(f'Config file: {config_path} loaded - {config}')
        config_version = config.get('versioning')

        prefix = config_version.get('prefix') if config_version else None
        incrementer = config_version.get('incrementer') if config_version else None
        tag = config_version.get('tag') if config_version else None
        initial_version = config_version.get('initial-version') if config_version else None

        # validate
        self.version_parser.validate_prefix(prefix)
        self.version_parser.validate_version(initial_version)
        self.version_tag_parser.validate_tag_name(tag)

        default_config.prefix = \
            prefix if prefix else default_config.prefix
        default_config.tag_config = \
            self.version_tag_parser.find_config_by_tag_name(tag) if tag else default_config.tag_config
        default_config.incrementer = \
            self.incrementer_parser.parse(incrementer) if incrementer else default_config.incrementer
        default_config.initial_version = \
            initial_version if initial_version else default_config.initial_version

        return default_config

    def merge(self, config_file: 'VersionConfig', config_cli_override: 'VersionConfig'):
        config_file.prefix = \
            config_cli_override.prefix if config_cli_override.prefix else config_file.prefix
        config_file.tag_config = \
            config_cli_override.tag_config if config_cli_override.tag_config else config_file.tag_config
        config_file.incrementer = \
            config_cli_override.incrementer if config_cli_override.incrementer else config_file.incrementer
        config_file.initial_version = \
            config_cli_override.initial_version if config_cli_override.initial_version else config_file.initial_version


class VersionConfig(object):
    prefix = ''
    incrementer = Incrementer.PATCH
    tag_config: TagConfig = None
    initial_version = '1.0.0'

    def __str__(self):
        return (f'prefix: {self.prefix}, '
                f'incrementer: {self.incrementer}, '
                f'tag: {self.tag_config}, '
                f'initial_version: {self.initial_version}')


class LoadConfigFileException(Exception):
    pass
