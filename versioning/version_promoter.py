from versioning.version import Version
from versioning.version_config import VersionConfig
from versioning.version_tag import VersionTag


class VersionPromoter(object):

    def promote(self, current_version: Version, config: VersionConfig) -> None:

        current_version.prefix = config.prefix

        if not config.tag_config:
            current_version.tag = None
            current_version.increment_version(config.incrementer)
            return

        if current_version.tag:
            if current_version.tag.name == config.tag_config.name and not config.tag_config.promotable:
                print(f'Tag {config.tag_config.name} not promotable - will keep same version')
                return

        new_tag = VersionTag()
        new_tag.name = config.tag_config.name
        new_tag.weight = config.tag_config.weight

        if config.tag_config.with_seq:
            new_tag.increase_seq()

        if not current_version.tag:
            current_version.increment_version(config.incrementer)
            current_version.tag = new_tag
            return

        if current_version.tag.name == new_tag.name and config.tag_config.with_seq:
            current_version.tag.increase_seq()
            return

        if current_version.tag.weight < new_tag.weight:
            current_version.tag = new_tag
            return

        if current_version.tag.seq and config.tag_config.with_seq:
            current_version.tag = new_tag
            return

        current_version.increment_version(config.incrementer)
        current_version.tag = new_tag
