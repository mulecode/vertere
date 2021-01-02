import pytest as pytest

from versioning.incrementer import Incrementer
from versioning.version_config import VersionConfig
from versioning.version_parser import VersionParser
from versioning.version_promoter import VersionPromoter
from versioning.version_tag_service import VersionTagLoader, VersionTagParser

from_scenario_1 = '1.2.3'
from_scenario_2 = '1.2.3.RELEASE'
from_scenario_3 = '1.2.3.RC3'
from_scenario_4 = '1.2.3.M10'
from_scenario_5 = '1.2.3.BUILD-SNAPSHOT'

NO_TAG = None
RELEASE = 'RELEASE'
RC = 'RC'
MILESTONE = 'M'
SNAPSHOT = 'BUILD-SNAPSHOT'
MAJOR = Incrementer.MAJOR
MINOR = Incrementer.MINOR
PATCH = Incrementer.PATCH


@pytest.mark.parametrize(
    'current,incrementer,tag,expected_value',
    [
        pytest.param(from_scenario_1, MAJOR, NO_TAG, 'v2.0.0',
                     id=f'{from_scenario_1} to {MAJOR} incrementer and {NO_TAG} tag'),
        pytest.param(from_scenario_2, MAJOR, NO_TAG, 'v2.0.0',
                     id=f'{from_scenario_2} to {MAJOR} incrementer and {NO_TAG} tag'),
        pytest.param(from_scenario_3, MAJOR, NO_TAG, 'v2.0.0',
                     id=f'{from_scenario_3} to {MAJOR} incrementer and {NO_TAG} tag'),
        pytest.param(from_scenario_4, MAJOR, NO_TAG, 'v2.0.0',
                     id=f'{from_scenario_4} to {MAJOR} incrementer and {NO_TAG} tag'),
        pytest.param(from_scenario_5, MAJOR, NO_TAG, 'v2.0.0',
                     id=f'{from_scenario_5} to {MAJOR} incrementer and {NO_TAG} tag'),

        pytest.param(from_scenario_1, MINOR, NO_TAG, 'v1.3.0',
                     id=f'{from_scenario_1} to {MINOR} incrementer and {NO_TAG} tag'),
        pytest.param(from_scenario_2, MINOR, NO_TAG, 'v1.3.0',
                     id=f'{from_scenario_2} to {MINOR} incrementer and {NO_TAG} tag'),
        pytest.param(from_scenario_3, MINOR, NO_TAG, 'v1.3.0',
                     id=f'{from_scenario_3} to {MINOR} incrementer and {NO_TAG} tag'),
        pytest.param(from_scenario_4, MINOR, NO_TAG, 'v1.3.0',
                     id=f'{from_scenario_4} to {MINOR} incrementer and {NO_TAG} tag'),
        pytest.param(from_scenario_5, MINOR, NO_TAG, 'v1.3.0',
                     id=f'{from_scenario_5} to {MINOR} incrementer and {NO_TAG} tag'),

        pytest.param(from_scenario_1, PATCH, NO_TAG, 'v1.2.4',
                     id=f'{from_scenario_1} to {PATCH} incrementer and {NO_TAG} tag'),
        pytest.param(from_scenario_2, PATCH, NO_TAG, 'v1.2.4',
                     id=f'{from_scenario_2} to {PATCH} incrementer and {NO_TAG} tag'),
        pytest.param(from_scenario_3, PATCH, NO_TAG, 'v1.2.4',
                     id=f'{from_scenario_3} to {PATCH} incrementer and {NO_TAG} tag'),
        pytest.param(from_scenario_4, PATCH, NO_TAG, 'v1.2.4',
                     id=f'{from_scenario_4} to {PATCH} incrementer and {NO_TAG} tag'),
        pytest.param(from_scenario_5, PATCH, NO_TAG, 'v1.2.4',
                     id=f'{from_scenario_5} to {PATCH} incrementer and {NO_TAG} tag'),

        pytest.param(from_scenario_1, MAJOR, RELEASE, 'v2.0.0.RELEASE',
                     id=f'{from_scenario_1} to {MAJOR} incrementer and {RELEASE} tag'),
        pytest.param(from_scenario_2, MAJOR, RELEASE, 'v2.0.0.RELEASE',
                     id=f'{from_scenario_2} to {MAJOR} incrementer and {RELEASE} tag'),
        pytest.param(from_scenario_3, MAJOR, RELEASE, 'v1.2.3.RELEASE',
                     id=f'{from_scenario_3} to {MAJOR} incrementer and {RELEASE} tag'),
        pytest.param(from_scenario_4, MAJOR, RELEASE, 'v1.2.3.RELEASE',
                     id=f'{from_scenario_4} to {MAJOR} incrementer and {RELEASE} tag'),
        pytest.param(from_scenario_5, MAJOR, RELEASE, 'v1.2.3.RELEASE',
                     id=f'{from_scenario_5} to {MAJOR} incrementer and {RELEASE} tag'),

        pytest.param(from_scenario_1, MINOR, RELEASE, 'v1.3.0.RELEASE',
                     id=f'{from_scenario_1} to {MINOR} incrementer and {RELEASE} tag'),
        pytest.param(from_scenario_2, MINOR, RELEASE, 'v1.3.0.RELEASE',
                     id=f'{from_scenario_2} to {MINOR} incrementer and {RELEASE} tag'),
        pytest.param(from_scenario_3, MINOR, RELEASE, 'v1.2.3.RELEASE',
                     id=f'{from_scenario_3} to {MINOR} incrementer and {RELEASE} tag'),
        pytest.param(from_scenario_4, MINOR, RELEASE, 'v1.2.3.RELEASE',
                     id=f'{from_scenario_4} to {MINOR} incrementer and {RELEASE} tag'),
        pytest.param(from_scenario_5, MINOR, RELEASE, 'v1.2.3.RELEASE',
                     id=f'{from_scenario_5} to {MINOR} incrementer and {RELEASE} tag'),

        pytest.param(from_scenario_1, PATCH, RELEASE, 'v1.2.4.RELEASE',
                     id=f'{from_scenario_1} to {PATCH} incrementer and {RELEASE} tag'),
        pytest.param(from_scenario_2, PATCH, RELEASE, 'v1.2.4.RELEASE',
                     id=f'{from_scenario_2} to {PATCH} incrementer and {RELEASE} tag'),
        pytest.param(from_scenario_3, PATCH, RELEASE, 'v1.2.3.RELEASE',
                     id=f'{from_scenario_3} to {PATCH} incrementer and {RELEASE} tag'),
        pytest.param(from_scenario_4, PATCH, RELEASE, 'v1.2.3.RELEASE',
                     id=f'{from_scenario_4} to {PATCH} incrementer and {RELEASE} tag'),
        pytest.param(from_scenario_5, PATCH, RELEASE, 'v1.2.3.RELEASE',
                     id=f'{from_scenario_5} to {PATCH} incrementer and {RELEASE} tag'),

        pytest.param(from_scenario_1, MAJOR, RC, 'v2.0.0.RC1',
                     id=f'{from_scenario_1} to {MAJOR} incrementer and {RC} tag'),
        pytest.param(from_scenario_2, MAJOR, RC, 'v2.0.0.RC1',
                     id=f'{from_scenario_2} to {MAJOR} incrementer and {RC} tag'),
        pytest.param(from_scenario_3, MAJOR, RC, 'v1.2.3.RC4',
                     id=f'{from_scenario_3} to {MAJOR} incrementer and {RC} tag'),
        pytest.param(from_scenario_4, MAJOR, RC, 'v1.2.3.RC1',
                     id=f'{from_scenario_4} to {MAJOR} incrementer and {RC} tag'),
        pytest.param(from_scenario_5, MAJOR, RC, 'v1.2.3.RC1',
                     id=f'{from_scenario_5} to {MAJOR} incrementer and {RC} tag'),

        pytest.param(from_scenario_1, MINOR, RC, 'v1.3.0.RC1',
                     id=f'{from_scenario_1} to {MINOR} incrementer and {RC} tag'),
        pytest.param(from_scenario_2, MINOR, RC, 'v1.3.0.RC1',
                     id=f'{from_scenario_2} to {MINOR} incrementer and {RC} tag'),
        pytest.param(from_scenario_3, MINOR, RC, 'v1.2.3.RC4',
                     id=f'{from_scenario_3} to {MINOR} incrementer and {RC} tag'),
        pytest.param(from_scenario_4, MINOR, RC, 'v1.2.3.RC1',
                     id=f'{from_scenario_4} to {MINOR} incrementer and {RC} tag'),
        pytest.param(from_scenario_5, MINOR, RC, 'v1.2.3.RC1',
                     id=f'{from_scenario_5} to {MINOR} incrementer and {RC} tag'),

        pytest.param(from_scenario_1, PATCH, RC, 'v1.2.4.RC1',
                     id=f'{from_scenario_1} to {PATCH} incrementer and {RC} tag'),
        pytest.param(from_scenario_2, PATCH, RC, 'v1.2.4.RC1',
                     id=f'{from_scenario_2} to {PATCH} incrementer and {RC} tag'),
        pytest.param(from_scenario_3, PATCH, RC, 'v1.2.3.RC4',
                     id=f'{from_scenario_3} to {PATCH} incrementer and {RC} tag'),
        pytest.param(from_scenario_4, PATCH, RC, 'v1.2.3.RC1',
                     id=f'{from_scenario_4} to {PATCH} incrementer and {RC} tag'),
        pytest.param(from_scenario_5, PATCH, RC, 'v1.2.3.RC1',
                     id=f'{from_scenario_5} to {PATCH} incrementer and {RC} tag'),

        pytest.param(from_scenario_1, MAJOR, MILESTONE, 'v2.0.0.M1',
                     id=f'{from_scenario_1} to {MAJOR} incrementer and {MILESTONE} tag'),
        pytest.param(from_scenario_2, MAJOR, MILESTONE, 'v2.0.0.M1',
                     id=f'{from_scenario_2} to {MAJOR} incrementer and {MILESTONE} tag'),
        pytest.param(from_scenario_3, MAJOR, MILESTONE, 'v1.2.3.M1',
                     id=f'{from_scenario_3} to {MAJOR} incrementer and {MILESTONE} tag'),
        pytest.param(from_scenario_4, MAJOR, MILESTONE, 'v1.2.3.M11',
                     id=f'{from_scenario_4} to {MAJOR} incrementer and {MILESTONE} tag'),
        pytest.param(from_scenario_5, MAJOR, MILESTONE, 'v1.2.3.M1',
                     id=f'{from_scenario_5} to {MAJOR} incrementer and {MILESTONE} tag'),

        pytest.param(from_scenario_1, MINOR, MILESTONE, 'v1.3.0.M1',
                     id=f'{from_scenario_1} to {MINOR} incrementer and {MILESTONE} tag'),
        pytest.param(from_scenario_2, MINOR, MILESTONE, 'v1.3.0.M1',
                     id=f'{from_scenario_2} to {MINOR} incrementer and {MILESTONE} tag'),
        pytest.param(from_scenario_3, MINOR, MILESTONE, 'v1.2.3.M1',
                     id=f'{from_scenario_3} to {MINOR} incrementer and {MILESTONE} tag'),
        pytest.param(from_scenario_4, MINOR, MILESTONE, 'v1.2.3.M11',
                     id=f'{from_scenario_4} to {MINOR} incrementer and {MILESTONE} tag'),
        pytest.param(from_scenario_5, MINOR, MILESTONE, 'v1.2.3.M1',
                     id=f'{from_scenario_5} to {MINOR} incrementer and {MILESTONE} tag'),

        pytest.param(from_scenario_1, PATCH, MILESTONE, 'v1.2.4.M1',
                     id=f'{from_scenario_1} to {PATCH} incrementer and {MILESTONE} tag'),
        pytest.param(from_scenario_2, PATCH, MILESTONE, 'v1.2.4.M1',
                     id=f'{from_scenario_2} to {PATCH} incrementer and {MILESTONE} tag'),
        pytest.param(from_scenario_3, PATCH, MILESTONE, 'v1.2.3.M1',
                     id=f'{from_scenario_3} to {PATCH} incrementer and {MILESTONE} tag'),
        pytest.param(from_scenario_4, PATCH, MILESTONE, 'v1.2.3.M11',
                     id=f'{from_scenario_4} to {PATCH} incrementer and {MILESTONE} tag'),
        pytest.param(from_scenario_5, PATCH, MILESTONE, 'v1.2.3.M1',
                     id=f'{from_scenario_5} to {PATCH} incrementer and {MILESTONE} tag'),

        pytest.param(from_scenario_1, MAJOR, SNAPSHOT, 'v2.0.0.BUILD-SNAPSHOT',
                     id=f'{from_scenario_1} to {MAJOR} incrementer and {SNAPSHOT} tag'),
        pytest.param(from_scenario_2, MAJOR, SNAPSHOT, 'v2.0.0.BUILD-SNAPSHOT',
                     id=f'{from_scenario_2} to {MAJOR} incrementer and {SNAPSHOT} tag'),
        pytest.param(from_scenario_3, MAJOR, SNAPSHOT, 'v2.0.0.BUILD-SNAPSHOT',
                     id=f'{from_scenario_3} to {MAJOR} incrementer and {SNAPSHOT} tag'),
        pytest.param(from_scenario_4, MAJOR, SNAPSHOT, 'v2.0.0.BUILD-SNAPSHOT',
                     id=f'{from_scenario_4} to {MAJOR} incrementer and {SNAPSHOT} tag'),
        pytest.param(from_scenario_5, MAJOR, SNAPSHOT, '1.2.3.BUILD-SNAPSHOT',
                     id=f'{from_scenario_5} to {MAJOR} incrementer and {SNAPSHOT} tag'),

        pytest.param(from_scenario_1, MINOR, SNAPSHOT, 'v1.3.0.BUILD-SNAPSHOT',
                     id=f'{from_scenario_1} to {MINOR} incrementer and {SNAPSHOT} tag'),
        pytest.param(from_scenario_2, MINOR, SNAPSHOT, 'v1.3.0.BUILD-SNAPSHOT',
                     id=f'{from_scenario_2} to {MINOR} incrementer and {SNAPSHOT} tag'),
        pytest.param(from_scenario_3, MINOR, SNAPSHOT, 'v1.3.0.BUILD-SNAPSHOT',
                     id=f'{from_scenario_3} to {MINOR} incrementer and {SNAPSHOT} tag'),
        pytest.param(from_scenario_4, MINOR, SNAPSHOT, 'v1.3.0.BUILD-SNAPSHOT',
                     id=f'{from_scenario_4} to {MINOR} incrementer and {SNAPSHOT} tag'),
        pytest.param(from_scenario_5, MINOR, SNAPSHOT, '1.2.3.BUILD-SNAPSHOT',
                     id=f'{from_scenario_5} to {MINOR} incrementer and {SNAPSHOT} tag'),

        pytest.param(from_scenario_1, PATCH, SNAPSHOT, 'v1.2.4.BUILD-SNAPSHOT',
                     id=f'{from_scenario_1} to {PATCH} incrementer and {SNAPSHOT} tag'),
        pytest.param(from_scenario_2, PATCH, SNAPSHOT, 'v1.2.4.BUILD-SNAPSHOT',
                     id=f'{from_scenario_2} to {PATCH} incrementer and {SNAPSHOT} tag'),
        pytest.param(from_scenario_3, PATCH, SNAPSHOT, 'v1.2.4.BUILD-SNAPSHOT',
                     id=f'{from_scenario_3} to {PATCH} incrementer and {SNAPSHOT} tag'),
        pytest.param(from_scenario_4, PATCH, SNAPSHOT, 'v1.2.4.BUILD-SNAPSHOT',
                     id=f'{from_scenario_4} to {PATCH} incrementer and {SNAPSHOT} tag'),
        pytest.param(from_scenario_5, PATCH, SNAPSHOT, '1.2.3.BUILD-SNAPSHOT',
                     id=f'{from_scenario_5} to {PATCH} incrementer and {SNAPSHOT} tag'),
    ],
)
def test_promote_with(current, incrementer, tag, expected_value):
    version_tag_loader = VersionTagLoader()
    version_tag_parser = VersionTagParser(
        version_tag_loader=version_tag_loader
    )
    version_parser = VersionParser(
        version_tag_parser=version_tag_parser
    )
    version_tag_parser.find_config_by_tag_name(tag)
    current_parsed = version_parser.parse(current)

    tag_config = version_tag_parser.find_config_by_tag_name(tag)
    version_config = given_version_config('v', incrementer, tag_config)

    promoter = VersionPromoter()
    promoter.promote(current_parsed, version_config)

    assert str(current_parsed) == expected_value


def given_version_config(prefix='', incrementer=Incrementer.PATCH, tag_config=None):
    version_config = VersionConfig()
    version_config.prefix = prefix
    version_config.incrementer = incrementer
    version_config.tag_config = tag_config
    return version_config
