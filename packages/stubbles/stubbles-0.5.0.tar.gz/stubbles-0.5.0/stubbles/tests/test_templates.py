import pytest
from stubbles.templates import _lines, _strip, _stubs, _whitespace, validate, populate, _is_stubble_line
from stubbles.types import Language


@pytest.mark.parametrize(
    'line,lang,desired',
    (
        ('// {{hello}}', Language.CPP, True),
        ('# Yolo', Language.PYTHON, False),
        ('# {{Yolo}}', Language.PYTHON, True),
        ('# Serial.printlln({{key}})', Language.PYTHON, True),
    )
)
def test_is_stubble_line(line, lang, desired):
    actual = _is_stubble_line(line=line, lang=lang)
    assert actual == desired


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

    actual = _lines(template=template, lang=Language.PYTHON)
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
    actual = _strip(line=string, lang=lang)
    assert actual == desired


@pytest.mark.parametrize(
    'string,desired,lang', (
            ('  # {{hello_there}}  ', '  ', Language.PYTHON),
            ('# {{hihi}}   ', '', Language.PYTHON),
            ('     // {{hihi}}   ', '     ', Language.CPP),
    )
)
def test_whitespace(string, desired, lang):
    actual = _whitespace(line=string, lang=lang)
    assert actual == desired


@pytest.mark.parametrize(
    'string,desired,lang', (
            ('  # {{hello_there}}  ', ['hello_there'], Language.PYTHON),
            ('# {{hihi}}   ', ['hihi'], Language.PYTHON),
            ('     // {{hihi}}   ', ['hihi'], Language.CPP),
            ('     // {{hihi}}  {{yesyes}}  ', ['hihi', 'yesyes'], Language.CPP),
            ('     // hihi  yesyes  ', [], Language.CPP),
    )
)
def test_stubs_single(string, desired, lang):
    actual = _stubs(line=string, lang=lang)
    assert actual == desired


def test_stubs_multi():
    string = '# {{hi}} {{there}}'
    actual = _stubs(line=string, lang=Language.PYTHON)
    desired = ['hi', 'there']
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


def test_replace():
    input_template = """
Hello there partner    
# {{key1}}
    # {{key2}}
\t#{{key3}}
"""
    desired = """
Hello there partner    
replacement1
    replacement2
\treplacement3
"""
    replacements = {
        'key1': 'replacement1',
        'key2': 'replacement2',
        'key3': 'replacement3',
    }
    actual = populate(template=input_template, lang=Language.PYTHON, replacements=replacements)
    assert actual == desired


def test_replace_inline():
    template = '// Serial.println({{key}});'
    replacements = {'key': 'val'}
    lang = Language.CPP
    actual = populate(template=template, lang=lang, replacements=replacements)
    desired = 'Serial.println(val);'
    assert actual == desired

