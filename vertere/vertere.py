import click

from vertere.git_repository import GitRepository
from vertere.incrementer import IncrementerParser
from vertere.version_config import VersionConfig, PromoterConfigLoader
from vertere.version_parser import VersionParser
from vertere.version_postfix_parser import VersionPostfixLoader, VersionPostfixParser
from vertere.version_promoter import VersionPromoter
from vertere.version_service import VersioningService
from vertere.version_storage import VersionStorage


@click.command()
@click.argument('action', default=None, type=click.Choice(['init', 'push', 'read']))
@click.option('--prefix', default=None, type=str)
@click.option('--incrementer', default=None, type=str)
@click.option('--postfix', default=None, type=str)
@click.option('--initial-version', default=None, type=str)
@click.option('--config-path', default=None, type=str)
@click.option('--debug', default=False, type=bool)
def cli(action, prefix, incrementer, postfix, initial_version, config_path, debug):
    try:

        # initialise IoC
        incrementer_parser = IncrementerParser()
        version_storage = VersionStorage()
        git_repository = GitRepository()

        version_postfix_loader = VersionPostfixLoader()
        version_postfix_parser = VersionPostfixParser(
            version_postfix_loader=version_postfix_loader
        )

        version_parser = VersionParser(
            version_postfix_parser=version_postfix_parser
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
            version_postfix_parser=version_postfix_parser,
            incrementer_parser=incrementer_parser
        )

        # Validate all cli inputs
        promoter_config_loader.validate_config_path(config_path)
        version_parser.validate_prefix(prefix)
        version_parser.validate_version(initial_version)
        version_postfix_parser.validate_postfix_name(postfix)

        config_cli_override = VersionConfig()
        config_cli_override.prefix = prefix
        config_cli_override.postfix_config = version_postfix_parser.find_postfix_config_by_name(postfix) if postfix else None
        config_cli_override.incrementer = incrementer_parser.parse(incrementer) if incrementer else None
        config_cli_override.initial_version = initial_version

        if debug:
            print(f'override config: {config_cli_override}')

        config = promoter_config_loader.load_config_from_file()
        if debug:
            print(f'config: {config}')

        promoter_config_loader.merge(config, config_cli_override)
        if debug:
            print(f'config merged: {config}')

        if action == 'read':
            click.echo(str(versioning_service.read()))

        if action == 'init':
            versioning_service.init(config)

        if action == 'push':
            versioning_service.push()

    except Exception as e:
        click.echo(f'Error! {e}')
        if debug:
            raise e
