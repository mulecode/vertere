from vertere.git_repository import GitRepository
from vertere.promoter_config import PromoterConfig
from vertere.version import Version
from vertere.version_parser import VersionParser
from vertere.version_promoter import VersionPromoter
from vertere.version_storage import VersionStorage


class VersioningService(object):
    def __init__(self, git_repository: GitRepository,
                 version_storage: VersionStorage,
                 version_parser: VersionParser,
                 version_promoter: VersionPromoter):
        self.git_repository = git_repository
        self.version_storage = version_storage
        self.version_parser = version_parser
        self.version_promoter = version_promoter

    def read(self):
        return self.version_storage.read()

    def push(self):
        current_version = self.version_storage.read()
        if not current_version:
            print(f'Cannot push - Nothing to push, Execute init command')
            return

        current_version_parsed = self.version_parser.parse(current_version)
        all_tags = self.git_repository.get_tags()

        if all_tags:
            high_version = self.__get_highest_semantic__(tags=all_tags)
            is_tag_head = self.git_repository.is_tag_head(str(high_version))
            if is_tag_head:
                print(f'Cannot push - Tag {high_version} is already in HEAD commit.')
                return

        postfix_name = current_version_parsed.postfix.name if current_version_parsed.postfix else None
        postfix_config = self.version_parser.get_version_postfix_parser().find_postfix_config_by_name(
            postfix_name
        )

        if postfix_config and not postfix_config.promotable and all_tags:
            print(f'Will delete tag {current_version} and tag again')
            self.git_repository.delete_tag(current_version)

        self.git_repository.tag(current_version)

    def init(self, version_config: PromoterConfig):
        self.git_repository.validate_git_initialised()
        all_tags = self.git_repository.get_tags()
        current_version = self.__get_highest_semantic__(tags=all_tags)
        if current_version:
            self.__apply_next_version__(current_version, version_config)
        else:
            self.__setup_new_version__(version_config)

    def __setup_new_version__(self, version_config: PromoterConfig):
        self.__require_non_none__(version_config.initial_version, 'initial_version is required.')
        print(f'Initialising project with version: {version_config.initial_version}')
        self.version_storage.persist(version_config.initial_version)

    def __apply_next_version__(self, current_version: Version, version_config: PromoterConfig):
        print(f'Found highest tag: {current_version}')
        self.__require_non_none__(version_config.incrementer, 'incrementer is required.')

        is_tag_head = self.git_repository.is_tag_head(str(current_version))
        if is_tag_head:
            print(f'Cannot versioning - Tag {current_version} is already in HEAD commit.')
            return
        self.version_promoter.promote(current_version, version_config)
        print(f'Next version {current_version}')
        self.version_storage.persist(current_version.__str__())

    def __get_highest_semantic__(self, tags):
        if not tags:
            return None
        git_tags_filtered = list(filter(lambda t: self.version_parser.is_version(t), tags))
        if not git_tags_filtered:
            return None
        tags_mapped = map(lambda v: self.version_parser.parse(v), git_tags_filtered)
        return sorted(tags_mapped, key=lambda t: t.to_hash(), reverse=True)[0]

    def __require_non_none__(self, value, error_message):
        if not value:
            raise InvalidInitParameterException(error_message)


class InvalidInitParameterException(Exception):
    """InvalidInitParameterException"""
    pass
