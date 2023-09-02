from stubbles.types import Language, comments
from typing import List, Dict, Mapping


START_STUBBLE = "{{"
END_STUBBLE = "}}"


def strip(line: str, lang: Language) -> str:
    comment = comments[lang]
    stripped_line = line.lstrip()  # Remove leading whitespaces
    bare_line = stripped_line.lstrip(comment).strip()
    return bare_line


def is_stubble_line(line: str, lang: Language) -> bool:
    stripped_line = strip(line=line, lang=lang)

    if stripped_line.startswith(START_STUBBLE) and stripped_line.endswith(END_STUBBLE):
        return True

    return False


def lines(template: str, lang: Language) -> List[str]:
    all_lines = template.split('\n')
    stubble_lines = []

    for line in all_lines:
        if is_stubble_line(line=line, lang=lang):
            stubble_lines.append(line)

    return stubble_lines


def stubble(line: str, lang: Language) -> str:
    if not is_stubble_line(line=line, lang=lang):
        raise ValueError("Line must be a valid stubble line.")

    stripped_line = strip(line=line, lang=lang)
    stub = stripped_line.removeprefix(START_STUBBLE).removesuffix(END_STUBBLE)
    return stub


def whitespace(line: str, lang: Language) -> str:
    if not is_stubble_line(line=line, lang=lang):
        raise ValueError("Line must be a valid stubble line.")

    comment = comments[lang]
    spaces, *rest = line.split(comment)
    return spaces


def validate(template: str, lang: Language, replacements: Mapping[str, str]):
    missing_keys = []

    all_lines = lines(template=template, lang=lang)
    stubbles = [stubble(line=line, lang=lang) for line in all_lines]

    for stub in stubbles:
        if stub not in replacements.keys():
            missing_keys.append(stub)
    if missing_keys:
        raise AssertionError(f"Replacements missing keys: {missing_keys}")


def replace(template: str, lang: Language, replacements: Dict[str, str]):
    pass