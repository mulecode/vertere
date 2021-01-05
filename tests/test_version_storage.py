import pytest

from vertere.version_storage import VersionStorage, FileNotFoundException


def test_when_file_exists_should_read_file_content(tmpdir):
    p = tmpdir.mkdir('out').join('output.txt')
    p.write("1.0.0")

    service = VersionStorage()
    service.output_file_name = p

    value = service.read()

    assert value == '1.0.0'


def test_when_file_not_exists_should_throw_exception():
    service = VersionStorage()
    service.output_file_name = 'invalid_file.txt'

    with pytest.raises(FileNotFoundException):
        service.read()
