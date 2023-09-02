import pytest
from stubbles.types import Language
from stubbles.inputs import language


@pytest.mark.parametrize(
    'extension,desired', (
        ('.c', Language.C),
        ('.cpp', Language.CPP),
        ('.py', Language.PYTHON),
        ('.java', Language.JAVA),
        ('.tsx', Language.TYPESCRIPT),
        ('.go', Language.GOLANG),

    )
)
def test_extensions(extension, desired):
    actual = language(extension)
    assert actual == desired