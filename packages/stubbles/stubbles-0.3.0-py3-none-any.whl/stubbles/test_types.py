import pytest
from stubbles.types import Language, extensions


def test_languages_unique():
    unique_extensions = set()
    for extension_list in extensions.values():
        for ext in extension_list:
            unique_extensions.add(ext)

    total_extensions = sum([len(ext) for ext in extensions.values()])
    assert total_extensions == len(unique_extensions)
