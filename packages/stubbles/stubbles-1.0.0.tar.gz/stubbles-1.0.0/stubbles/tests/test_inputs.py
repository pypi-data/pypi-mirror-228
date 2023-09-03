import pytest
import json
from stubbles.types import Language
from stubbles.inputs import language, read_file_to_dict, _is_excludable_file, list_files
from pathlib import Path


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


def test_read_json_file(tmp_path):
    p = tmp_path / "test.json"
    p.write_text(json.dumps({"key": "value"}))
    assert read_file_to_dict(str(p)) == {"key": "value"}


def test_read_xml_file(tmp_path):
    p = tmp_path / "test.xml"
    p.write_text("<root><key>value</key></root>")
    assert read_file_to_dict(str(p)) == {"key": "value"}


def test_read_yaml_file(tmp_path):
    p = tmp_path / "test.yaml"
    p.write_text("key: value")
    assert read_file_to_dict(str(p)) == {"key": "value"}


def test_read_toml_file(tmp_path):
    p = tmp_path / "test.toml"
    p.write_text("key = \"value\"")
    assert read_file_to_dict(str(p)) == {"key": "value"}


def test_read_ini_file(tmp_path):
    p = tmp_path / "test.ini"
    p.write_text("[section]\nkey=value")
    assert read_file_to_dict(str(p)) == {"section": {"key": "value"}}


def test_read_csv_file(tmp_path):
    p = tmp_path / "test.csv"
    p.write_text("key,value\nkey1,val1")
    assert read_file_to_dict(str(p)) == {"key1": "val1"}


def test_read_unsupported_file(tmp_path):
    p = tmp_path / "test.txt"
    p.write_text("this is a text file")
    with pytest.raises(ValueError):
        read_file_to_dict(str(p))


def test_read_nonexistent_file(tmp_path):
    p = tmp_path / "does_not_exist.xyz"
    with pytest.raises(Exception):
        read_file_to_dict(str(p))


@pytest.mark.parametrize(
    'filename,desired',
    [
        (Path('__pycache__'), True),
        (Path('file.swp'), True),
        (Path('.hello.ini'), True),
        (Path('there.py'), False),
        (Path('DS_Store~'), True),
        (Path('yolo.cpp'), False),
    ]
)
def test_is_excludable(filename, desired):
    actual = _is_excludable_file(filename)
    assert actual == desired


def test_list_files(tmp_path):
    system_files = ['.sys.ini', 'DS_Store~', '__pycache__']
    desired_files = ['hello.py', 'yolo.cpp', 'blue.h']
    all_files = system_files + desired_files
    for filename in all_files:
        full_path = tmp_path / filename
        with open(full_path, 'w') as file:
            file.write('nothing')

    actual = set(list_files(tmp_path))
    assert set([tmp_path / file for file in desired_files]) == actual
