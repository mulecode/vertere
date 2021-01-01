import pytest

from versioning.version_incrementer import IncrementerParser, InvalidIncrementTypeException


@pytest.mark.parametrize(
    'value,expected_value,expected_name',
    [
        pytest.param('PATCH', 1, 'PATCH', id='with patch upper cased'),
        pytest.param('patch', 1, 'PATCH', id='with forward lower cased'),
        pytest.param('Patch', 1, 'PATCH', id='with forward capitalised'),
        pytest.param('MINOR', 2, 'MINOR', id='with patch upper cased'),
        pytest.param('minor', 2, 'MINOR', id='with forward lower cased'),
        pytest.param('Minor', 2, 'MINOR', id='with forward capitalised'),
        pytest.param('MAJOR', 3, 'MAJOR', id='with patch upper cased'),
        pytest.param('major', 3, 'MAJOR', id='with forward lower cased'),
        pytest.param('Major', 3, 'MAJOR', id='with forward capitalised'),
        pytest.param(' Major ', 3, 'MAJOR', id='with trail blank space')
    ],
)
def test_incrementer_parser(value, expected_value, expected_name):
    incrementer_parser = IncrementerParser()
    incrementer = incrementer_parser.parse(value)

    assert incrementer.name == expected_name
    assert incrementer.value == expected_value


@pytest.mark.parametrize(
    'value,expected_exception',
    [
        pytest.param('invalid', InvalidIncrementTypeException, id='with invalid name'),
        pytest.param(' ', InvalidIncrementTypeException, id='with empty name'),
        pytest.param(True, InvalidIncrementTypeException, id='with True')
    ],
)
def test_incrementer_parser_should_raise_exception(value, expected_exception):
    incrementer_parser = IncrementerParser()

    with pytest.raises(expected_exception):
        incrementer_parser.parse(value)


@pytest.mark.parametrize(
    'value,expected_result',
    [
        pytest.param(None, None, id='with None'),
        pytest.param(False, None, id='with False')
    ],
)
def test_incrementer_parser_should_not_parse(value, expected_result):
    incrementer_parser = IncrementerParser()

    result = incrementer_parser.parse(value)

    assert result == expected_result
