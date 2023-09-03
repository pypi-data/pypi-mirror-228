import sys

import pytest
import os
import json
import subprocess
from pathlib import Path
from shutil import copytree
from stubbles.inputs import list_files
from stubbles.__main__ import main  # Replace 'your_module' with the actual module name containing main()


data_dir = Path(os.path.dirname(os.path.abspath(__file__))) / 'data'



def test_main_with_file_template(tmp_path):
    filename = 'example.cpp'
    template = data_dir / filename
    replacements_path = tmp_path / "replacements.json"
    replacements = {'replacement': 'hello_there'}
    with open(replacements_path, 'w') as replacements_file:
        replacements_file.write(json.dumps(replacements))

    output_dir = tmp_path / "generated"
    output_path = output_dir / filename

    main(template=template, replacements_file=replacements_path, output_dir=output_dir)
    with open(output_path, 'r') as output_file:
        contents = output_file.read()

    assert (output_dir / filename).exists()
    assert replacements['replacement'] in contents


def test_main_with_directory_template(tmp_path):
    template = data_dir
    replacements_path = tmp_path / "replacements.json"
    replacements = {'replacement': 'hello_there'}
    with open(replacements_path, 'w') as replacements_file:
        replacements_file.write(json.dumps(replacements))

    output_dir = tmp_path / "generated"

    main(template=template, replacements_file=replacements_path, output_dir=output_dir)

    input_files = list_files(data_dir)
    output_files = list_files(output_dir)
    assert set([file.name for file in input_files]) == set([file.name for file in output_files])

    for file_path in output_files:
        with open(file_path, 'r') as output_file:
            contents = output_file.read()
            assert replacements['replacement'] in contents


def test_main_from_command_line(tmp_path):
    template = data_dir
    replacements_path = tmp_path / "replacements.json"
    replacements = {'replacement': 'hello_there'}
    with open(replacements_path, 'w') as replacements_file:
        replacements_file.write(json.dumps(replacements))

    output_dir = tmp_path / "generated"
    result = subprocess.run([
        sys.executable, '-m', 'stubbles',
        '--template', template,
        '--replacements', replacements_path,
        '--output-dir', output_dir,
    ])

    input_files = list_files(data_dir)
    output_files = list_files(output_dir)

    assert set([file.name for file in output_files]) == set([file.name for file in input_files])

    for file_path in output_files:
        with open(file_path, 'r') as output_file:
            contents = output_file.read()
            assert replacements['replacement'] in contents

