import pytest

from vertere.version_parser import VersionParser
from vertere.version_postfix_loader import VersionPostfixLoader
from vertere.version_postfix_parser import VersionPostfixParser


@pytest.mark.parametrize(
    'value',
    [
        pytest.param('1.2.3', id='simple scenario'),
        pytest.param('v1.2.3', id='simple scenario with prefix'),
        pytest.param('1.2.3.BUILD-SNAPSHOT', id='with postfix BUILD-SNAPSHOT'),
        pytest.param('1.2.3.M4', id='with postfix M'),
        pytest.param('1.2.3.RC5', id='with postfix RC'),
        pytest.param('1.2.3.RELEASE', id='with postfix RELEASE'),
    ],
)
def test_version_parse(value):
    version_postfix_loader = VersionPostfixLoader()
    version_postfix_parser = VersionPostfixParser(
        version_postfix_loader=version_postfix_loader
    )
    version_parser = VersionParser(
        version_postfix_parser=version_postfix_parser
    )
    version = version_parser.parse(value)

    assert version.__str__() == value


@pytest.mark.parametrize(
    'value, expected',
    [
        pytest.param('1.2.3', True, id='simple scenario'),
        pytest.param('v1.2.3', True, id='simple scenario with prefix'),
        pytest.param('1.2.3.BUILD-SNAPSHOT', True, id='with postfix BUILD-SNAPSHOT'),
        pytest.param('1.2.3.M4', True, id='with postfix M'),
        pytest.param('1.2.3.RC5', True, id='with postfix RC'),
        pytest.param('1.2.3.RELEASE', True, id='with postfix RELEASE'),
        pytest.param('v.1.2.3.RELEASE', False, id='with invalid prefix 1'),
        pytest.param('v 1.2.3.RELEASE', False, id='with invalid prefix 2'),
        pytest.param('1.2', False, id='with invalid semantic'),
        pytest.param('1.2,3', False, id='with invalid semantic with comma'),
        pytest.param('1.2.3.SNAPSHOT', False, id='with invalid postfix'),
        pytest.param('1.2.3.RELEASE2', False, id='with misplaced sequencer'),
        pytest.param('1.2.3.RC', False, id='without required sequencer'),
        pytest.param('1.2.3.M0', False, id='with invalid sequencer'),
    ],
)
def test_check_is_version(value, expected):
    version_postfix_loader = VersionPostfixLoader()
    version_postfix_parser = VersionPostfixParser(
        version_postfix_loader=version_postfix_loader
    )
    version_parser = VersionParser(
        version_postfix_parser=version_postfix_parser
    )
    is_version = version_parser.is_version(value)

    assert is_version == expected
