from vertere.version_service import VersioningService


def test_when_command_read_should_return_value(mocker):
    mocked_version_storage = mocker.Mock()
    mocked_version_storage('read')
    mocked_version_storage.read.return_value = '1.0.0'

    service = VersioningService(
        git_repository=None,
        version_storage=mocked_version_storage,
        version_parser=None,
        version_promoter=None
    )

    value = service.read()

    mocked_version_storage.read.assert_called_once()
    assert value == '1.0.0'
