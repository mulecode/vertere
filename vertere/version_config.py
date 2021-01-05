import yaml
from os import path

from vertere.incrementer import Incrementer, IncrementerParser
from vertere.version_parser import VersionParser
from vertere.version_postfix_parser import PostfixConfig, VersionPostfixParser


class PromoterConfigLoader(object):
    config_file_name = 'vertere.yml'

    def __init__(self, version_parser: VersionParser,
                 version_postfix_parser: VersionPostfixParser,
                 incrementer_parser: IncrementerParser):
        self.version_parser = version_parser
        self.version_postfix_parser = version_postfix_parser
        self.incrementer_parser = incrementer_parser

    def validate_config_path(self, config_path: str):
        if not config_path:
            return
        config_exists = path.exists(config_path)
        if not config_exists:
            raise LoadConfigFileException(f'Error loading config file {config_path} - File does not exists')

    def load_config_from_file(self, config_path: str = config_file_name) -> 'PromoterConfig':

        config_path = config_path if config_path else self.config_file_name

        default_config = PromoterConfig()

        config_exists = path.exists(config_path)
        if not config_exists:
            return default_config

        config = yaml.safe_load(open(config_path))
        config_version = config.get('versioning')

        prefix = config_version.get('prefix') if config_version else None
        incrementer = config_version.get('incrementer') if config_version else None
        postfix = config_version.get('postfix') if config_version else None
        initial_version = config_version.get('initial-version') if config_version else None

        # validate
        self.version_parser.validate_prefix(prefix)
        self.version_parser.validate_version(initial_version)
        self.version_postfix_parser.validate_postfix_name(postfix)

        default_config.prefix = \
            prefix if prefix else default_config.prefix
        default_config.postfix_config = \
            self.version_postfix_parser.find_postfix_config_by_name(postfix) if postfix else default_config.postfix_config
        default_config.incrementer = \
            self.incrementer_parser.parse(incrementer) if incrementer else default_config.incrementer
        default_config.initial_version = \
            initial_version if initial_version else default_config.initial_version

        return default_config

    def merge(self, config_file: 'PromoterConfig', config_cli_override: 'PromoterConfig'):
        config_file.prefix = \
            config_cli_override.prefix if config_cli_override.prefix else config_file.prefix
        config_file.postfix_config = \
            config_cli_override.postfix_config if config_cli_override.postfix_config else config_file.postfix_config
        config_file.incrementer = \
            config_cli_override.incrementer if config_cli_override.incrementer else config_file.incrementer
        config_file.initial_version = \
            config_cli_override.initial_version if config_cli_override.initial_version else config_file.initial_version


class PromoterConfig(object):
    prefix = ''
    incrementer = Incrementer.PATCH
    postfix_config: PostfixConfig = None
    initial_version = '1.0.0'

    def __str__(self):
        return (f'prefix: {self.prefix}, '
                f'incrementer: {self.incrementer}, '
                f'postfix_config: {self.postfix_config}, '
                f'initial_version: {self.initial_version}')


class LoadConfigFileException(Exception):
    pass
