from vertere.promoter_config import PromoterConfig
from vertere.version import Version
from vertere.version_postfix import VersionPostfix


class VersionPromoter(object):

    def promote(self, current_version: Version, config: PromoterConfig) -> None:

        if current_version.postfix and config.postfix_config:
            if current_version.postfix.name == config.postfix_config.name and not config.postfix_config.promotable:
                print(f'Postfix {config.postfix_config.name} not promotable - will keep same version')
                return

        current_version.prefix = config.prefix

        if not config.postfix_config:
            current_version.postfix = None
            current_version.increment_version(config.incrementer)
            return

        new_postfix = VersionPostfix()
        new_postfix.name = config.postfix_config.name
        new_postfix.weight = config.postfix_config.weight

        if config.postfix_config.with_seq:
            new_postfix.increase_seq()

        if not current_version.postfix:
            current_version.increment_version(config.incrementer)
            current_version.postfix = new_postfix
            return

        if current_version.postfix.name == new_postfix.name and config.postfix_config.with_seq:
            current_version.postfix.increase_seq()
            return

        if current_version.postfix.weight < new_postfix.weight:
            current_version.postfix = new_postfix
            return

        if current_version.postfix.seq and config.postfix_config.with_seq:
            current_version.postfix = new_postfix
            return

        current_version.increment_version(config.incrementer)
        current_version.postfix = new_postfix
