import click

from vertere.git_repository import GitRepository
from vertere.incrementer import IncrementerParser, Incrementer
from vertere.promoter_config import PromoterConfigLoader, PromoterConfig
from vertere.version_parser import VersionParser
from vertere.version_postfix_parser import VersionPostfixLoader, VersionPostfixParser
from vertere.version_promoter import VersionPromoter
from vertere.version_service import VersioningService
from vertere.version_storage import VersionStorage

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


def validate_prefix(ctx, param, value):
    try:
        version_parser.validate_prefix(value)
        return value
    except Exception:
        raise click.BadParameter(f'Prefix {value} should contain letters only.')


def validate_config_path(ctx, param, value):
    try:
        promoter_config_loader.validate_config_path(value)
        return value
    except Exception:
        raise click.BadParameter(f'File {value} does not exists.')


def validate_postfix(ctx, param, value):
    try:
        version_postfix_parser.validate_postfix_name(value)
        return version_postfix_parser.find_postfix_config_by_name(value) if value else None
    except Exception:
        raise click.BadParameter(f'Postfix {value} does not exists.')


def validate_incrementer(ctx, param, value):
    try:
        return incrementer_parser.parse(value) if value else None
    except Exception:
        raise click.BadParameter(f'Incrementer {value} does not exists.')


def validate_initial_version(ctx, param, value):
    try:
        version_parser.validate_version(value)
        return value
    except Exception:
        raise click.BadParameter(f'Incrementer {value} does not exists.')


help_initial_version = 'Required when a project has not been yet initialised.' \
                       ' It will determine the initial version for a git project.' \
                       ' Default value: 1.0.0'

help_prefix = 'Optional property that sets a prefix for a version. ' \
              ' Default value: '' (empty string)' \
              ' Example.: when --prefix=v, the version will be displayed as v1.2.3'

help_incrementer = 'Value that dictates how the next version will be incremented.' \
                   ' Default value: PATCH'

help_postfix = 'Optional property that can be used to append a known postfix to the version.' \
               ' It supports [BUILD-SNAPSHOT, M, RC and RELEASE].' \
               ' Example: --postfix=RELEASE, the next version will be displayed as 1.2.3.RELEASE.'

help_config_path = 'Optional property, used to point to vertere file configuration.' \
                   ' Default value: vertere.yml'

help_debug = 'Enables extra log lines while executing this program.' \
             ' it might help to identify a possible problem.' \
             ' Default value: false'


@click.command()
@click.argument('action', default=None,
                type=click.Choice(['init', 'push', 'read']))
@click.option('--prefix', default=None, type=str,
              callback=validate_prefix, help=help_prefix)
@click.option('--incrementer', default=None,
              type=click.Choice(Incrementer.__members__, case_sensitive=False),
              callback=validate_incrementer, help=help_incrementer)
@click.option('--postfix', default=None, type=str,
              callback=validate_postfix, help=help_postfix)
@click.option('--initial-version', default=None, type=str,
              callback=validate_initial_version, help=help_initial_version)
@click.option('--config-path', default=None, type=str,
              callback=validate_config_path, help=help_config_path)
@click.option('--debug', default=False, type=bool, help=help_debug)
def cli(action, prefix, incrementer, postfix, initial_version, config_path, debug):
    try:

        config_cli_override = PromoterConfig()
        config_cli_override.prefix = prefix
        config_cli_override.postfix_config = postfix
        config_cli_override.incrementer = incrementer
        config_cli_override.initial_version = initial_version

        if debug:
            print(f'override config: {config_cli_override}')

        config = promoter_config_loader.load_config_from_file(config_path)
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
