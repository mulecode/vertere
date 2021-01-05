from vertere.version_postfix import VersionPostfix
from vertere.version_postfix_loader import VersionPostfixLoader, PostfixConfig


class VersionPostfixParser(object):
    def __init__(self, version_postfix_loader: VersionPostfixLoader):
        self.version_postfix_loader = version_postfix_loader

    def validate_postfix_name(self, postfix_name: str):
        if not postfix_name:
            return
        if not self.find_postfix_config_by_name(postfix_name):
            raise InvalidVersionPostfixException(
                f'Unpassable postfix {postfix_name}. available options: [{self.get_postfixes_joined()}]'
            )

    def find_postfix_config_by_name(self, postfix_name) -> 'PostfixConfig':
        configured_postfixes = self.version_postfix_loader.get_all_postfix_configuration()
        return next(
            filter(
                lambda t: t.name == postfix_name, configured_postfixes
            ), None)

    def get_postfixes_joined(self) -> str:
        configured_postfixes = self.version_postfix_loader.get_all_postfix_configuration()
        postfix_list = map(lambda t: t.name, configured_postfixes)
        return ', '.join(postfix_list)

    def count(self) -> int:
        configured_postfixes = self.version_postfix_loader.get_all_postfix_configuration()
        return len(list(configured_postfixes))

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

    def is_valid(self, postfix_name, seq) -> bool:
        postfix_config = self.find_postfix_config_by_name(postfix_name)

        if not postfix_config:
            return False

        if postfix_config.with_seq and seq is None:
            return False

        if postfix_config.with_seq and (seq is not None and int(seq) <= 0):
            return False

        if not postfix_config.with_seq and seq is not None:
            return False

        return True


class InvalidVersionPostfixException(Exception):
    """Invalid version postfix"""
    pass
