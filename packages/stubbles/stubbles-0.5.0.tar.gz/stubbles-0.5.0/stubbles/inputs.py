from stubbles.types import Language, extensions
import json
import os
import csv
import configparser
import xml.etree.ElementTree as ET
import yaml
import toml


def language(extension: str) -> Language:
    for lang, exts in extensions.items():
        if extension in exts:
            return lang

    raise ValueError(f"Language not found for extension {extension}.")


def read_file_to_dict(filepath):
    file_ext = os.path.splitext(filepath)[-1]
    output_dict = {}

    if file_ext == '.json':
        with open(filepath, 'r') as f:
            output_dict = json.load(f)

    elif file_ext == '.xml':
        tree = ET.parse(filepath)
        root = tree.getroot()
        for elem in root:
            output_dict[elem.tag] = elem.text

    elif file_ext == '.yaml' or file_ext == '.yml':
        with open(filepath, 'r') as f:
            output_dict = yaml.safe_load(f)

    elif file_ext == '.toml':
        output_dict = toml.load(filepath)

    elif file_ext == '.ini':
        config = configparser.ConfigParser()
        config.read(filepath)
        for section in config.sections():
            output_dict[section] = {}
            for key, val in config.items(section):
                output_dict[section][key] = val

    elif file_ext == '.csv':
        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if header:
                for row in reader:
                    key = row[0]
                    value = row[1]
                    output_dict[key] = value

    else:
        raise ValueError(f"Unsupported file extension: {file_ext}")

    return output_dict
