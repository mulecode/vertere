import click

from versioning.incrementer import IncrementerParser
from versioning.version_config import VersionConfig, PromoterConfigLoader
from versioning.version_git_repository import GitRepository
from versioning.version_parser import VersionParser
from versioning.version_promoter import VersionPromoter
from versioning.version_service import VersioningService
from versioning.version_storage import VersionStorage
from versioning.version_tag_service import VersionTagLoader, VersionTagParser


@click.command()
@click.argument('action', default=None, type=click.Choice(['init', 'push', 'read']))
@click.option('--prefix', default=None, type=str)
@click.option('--incrementer', default=None, type=str)
@click.option('--tag', default=None, type=str)
@click.option('--initial-version', default=None, type=str)
@click.option('--config-path', default=None, type=str)
@click.option('--debug', default=False, type=bool)
def cli(action, prefix, incrementer, tag, initial_version, config_path, debug):
    try:

        # initialise IoC
        incrementer_parser = IncrementerParser()
        version_storage = VersionStorage()
        git_repository = GitRepository()

        version_tag_loader = VersionTagLoader()
        version_tag_parser = VersionTagParser(
            version_tag_loader=version_tag_loader
        )

        version_parser = VersionParser(
            version_tag_parser=version_tag_parser
        )
        version_promoter = VersionPromoter()
        versioning_service = VersioningService(
            git_repository=git_repository,
            version_storage=version_storage,
            version_parser=version_parser,
            version_promoter=version_promoter
        )
        promoter_config_loader = PromoterConfigLoader(
            version_parser=version_parser,
            version_tag_parser=version_tag_parser,
            incrementer_parser=incrementer_parser
        )

        # Validate all cli inputs
        promoter_config_loader.validate_config_path(config_path)
        version_parser.validate_prefix(prefix)
        version_parser.validate_version(initial_version)
        version_tag_parser.validate_tag_name(tag)

        config_cli_override = VersionConfig()
        config_cli_override.prefix = prefix
        config_cli_override.tag_config = version_tag_parser.find_config_by_tag_name(tag) if tag else None
        config_cli_override.incrementer = incrementer_parser.parse(incrementer) if incrementer else None
        config_cli_override.initial_version = initial_version
        print(f'override config: {config_cli_override}')

        config = promoter_config_loader.load_config_from_file()
        print(f'config: {config}')

        promoter_config_loader.merge(config, config_cli_override)

        print(f'config merged: {config}')
        if action == 'read':
            click.echo(
                str(versioning_service.read())
            )

        if action == 'init':
            versioning_service.init(config)

        if action == 'push':
            versioning_service.push()

    except Exception as e:
        click.echo(f'Error! {e}')
        raise e
