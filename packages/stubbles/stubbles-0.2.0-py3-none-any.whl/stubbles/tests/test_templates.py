import pytest
from stubbles.templates import lines, strip, stubble, whitespace, validate
from stubbles.types import Language


def test_lines_python():
    template = """
    # {{replacement_code}}
    print("Hello, world!")  # This is a comment
    #
# {{other_replacement_code}}
    \t#
        # This is an indented comment
        print("Indented code")
    \t\t\t#
"""

    actual = lines(template=template, lang=Language.PYTHON)
    desired = [
        "    # {{replacement_code}}",
        "# {{other_replacement_code}}"
    ]
    assert actual == desired


@pytest.mark.parametrize(
    'string,desired,lang', (
        ('  # {{hello_there}}  ', '{{hello_there}}', Language.PYTHON),
        ('# {{hihi}}   ', '{{hihi}}', Language.PYTHON),
        ('     // {{hihi}}   ', '{{hihi}}', Language.CPP),
    )
)
def test_strip(string, desired, lang):
    actual = strip(line=string, lang=lang)
    assert actual == desired


@pytest.mark.parametrize(
    'string,desired,lang', (
            ('  # {{hello_there}}  ', '  ', Language.PYTHON),
            ('# {{hihi}}   ', '', Language.PYTHON),
            ('     // {{hihi}}   ', '     ', Language.CPP),
    )
)
def test_whitespace(string, desired, lang):
    actual = whitespace(line=string, lang=lang)
    assert actual == desired


@pytest.mark.parametrize(
    'string,desired,lang', (
            ('  # {{hello_there}}  ', 'hello_there', Language.PYTHON),
            ('# {{hihi}}   ', 'hihi', Language.PYTHON),
            ('     // {{hihi}}   ', 'hihi', Language.CPP),
    )
)
def test_stubble(string, desired, lang):
    actual = stubble(line=string, lang=lang)
    assert actual == desired


def test_validate_raises():
    template = '{{hello}}'
    replacements = {'goodbye': 'hello'}
    with pytest.raises(AssertionError):
        validate(template=template, lang=Language.PYTHON, replacements=replacements)


def test_validate_ok():
    template = '{{hello}}'
    replacements = {'hello': 'hello'}
    validate(template=template, lang=Language.PYTHON, replacements=replacements)
