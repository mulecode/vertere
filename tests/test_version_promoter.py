from versioning.version import Version
from versioning.version_config import VersionConfig
from versioning.version_incrementer import Incrementer
from versioning.version_promoter import VersionPromoter
from versioning.version_tag import VersionTag
from versioning.version_tag_service import TagConfig


def test_given_version_numbers_only_should_promote_patch(mocker):
    promoter = VersionPromoter()

    current_version = given_version('', 1, 2, 3, None)
    version_config = given_version_config('', Incrementer.PATCH, None)

    promoter.promote(current_version, version_config)

    assert str(current_version) == '1.2.4'


def test_given_version_numbers_only_should_promote_minor(mocker):
    promoter = VersionPromoter()

    current_version = given_version('', 1, 2, 3, None)
    version_config = given_version_config('', Incrementer.MINOR, None)

    promoter.promote(current_version, version_config)

    assert str(current_version) == '1.3.0'


def test_given_version_numbers_only_should_promote_major(mocker):
    promoter = VersionPromoter()

    current_version = given_version('', 1, 2, 3, None)
    version_config = given_version_config('', Incrementer.MAJOR, None)

    promoter.promote(current_version, version_config)

    assert str(current_version) == '2.0.0'


def test_given_version_no_prefix_should_promote_major_with_prefix(mocker):
    promoter = VersionPromoter()

    current_version = given_version('', 1, 2, 3, None)
    version_config = given_version_config('v', Incrementer.MAJOR, None)

    promoter.promote(current_version, version_config)

    assert str(current_version) == 'v2.0.0'


def test_given_version_no_tag_should_promote_major_with_tag(mocker):
    promoter = VersionPromoter()

    current_version = given_version('', 1, 2, 3, None)
    tag_config = given_tag_config('RELEASE', 4, False, True)
    version_config = given_version_config('v', Incrementer.MAJOR, tag_config)

    promoter.promote(current_version, version_config)

    assert str(current_version) == 'v2.0.0.RELEASE'


def test_given_version_no_tag_should_promote_major_with_tag_seq(mocker):
    promoter = VersionPromoter()

    current_version = given_version('', 1, 2, 3, None)
    tag_config = given_tag_config('RC', 3, True, True)
    version_config = given_version_config('v', Incrementer.MAJOR, tag_config)

    promoter.promote(current_version, version_config)

    assert str(current_version) == 'v2.0.0.RC1'


def test_given_version_tag_no_seq_should_promote_major_with_tag_no_seq(mocker):
    promoter = VersionPromoter()

    version_tag = given_tag('RELEASE', 4, 0)
    current_version = given_version('', 1, 2, 3, version_tag)
    tag_config = given_tag_config('RELEASE', 4, False, True)
    version_config = given_version_config('v', Incrementer.MAJOR, tag_config)

    promoter.promote(current_version, version_config)

    assert str(current_version) == 'v2.0.0.RELEASE'


def test_given_version_tag_seq_should_promote_major_with_tag_seq(mocker):
    promoter = VersionPromoter()

    version_tag = given_tag('RC', 3, 16)
    current_version = given_version('', 1, 2, 3, version_tag)
    tag_config = given_tag_config('RC', 3, True, True)
    version_config = given_version_config('v', Incrementer.MAJOR, tag_config)

    promoter.promote(current_version, version_config)

    assert str(current_version) == 'v1.2.3.RC17'


def test_given_version_tag_seq_should_promote_major_with_tag_no_seq(mocker):
    promoter = VersionPromoter()

    version_tag = given_tag('M', 2, 16)
    current_version = given_version('', 1, 2, 3, version_tag)
    tag_config = given_tag_config('RC', 3, True, True)
    version_config = given_version_config('v', Incrementer.MAJOR, tag_config)

    promoter.promote(current_version, version_config)

    assert str(current_version) == 'v1.2.3.RC1'

def test_given_version_tag_seq_should_promote_major_with_tag_no_seq(mocker):
    promoter = VersionPromoter()

    version_tag = given_tag('BUILD-SNAPSHOT', 1, 0)
    current_version = given_version('', 1, 2, 3, version_tag)
    tag_config = given_tag_config('BUILD-SNAPSHOT', None, False, False)
    version_config = given_version_config('v', Incrementer.MAJOR, tag_config)

    promoter.promote(current_version, version_config)

    assert str(current_version) == '1.2.3.BUILD-SNAPSHOT'

def test_given_version_with_tag_should_promote_major_with_no_tag(mocker):
    promoter = VersionPromoter()

    version_tag = given_tag('RELEASE', 4, 0)
    current_version = given_version('', 1, 2, 3, version_tag)
    version_config = given_version_config('v', Incrementer.MAJOR, None)

    promoter.promote(current_version, version_config)

    assert str(current_version) == 'v2.0.0'


def given_tag(name='', weight=1, seq=1):
    version_tag = VersionTag()
    version_tag.name = name
    version_tag.weight = weight
    version_tag.seq = seq
    return version_tag


def given_version_config(prefix='', incrementer=Incrementer.PATCH, tag_config=None):
    version_config = VersionConfig()
    version_config.prefix = prefix
    version_config.incrementer = incrementer
    version_config.tag_config = tag_config
    return version_config


def given_tag_config(name='', weight=1, with_seq=False, promotable=False):
    tag_config = TagConfig()
    tag_config.name = name
    tag_config.weight = weight
    tag_config.with_seq = with_seq
    tag_config.promotable = promotable
    return tag_config


def given_version(prefix='', major=1, minor=2, patch=3, tag=None):
    current_version = Version()
    current_version.prefix = prefix
    current_version.major = major
    current_version.minor = minor
    current_version.patch = patch
    current_version.tag = tag
    return current_version
