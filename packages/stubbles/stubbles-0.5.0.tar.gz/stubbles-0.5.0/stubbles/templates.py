from stubbles.types import Language, comments
from typing import List, Dict, Mapping, Tuple, Any
from copy import copy
import itertools


def populate(template: str, lang: Language, replacements: Dict[str, str]) -> str:
    all_lines = template.split('\n')
    new_lines = []
    for line in all_lines:
        if _is_stubble_line(line=line, lang=lang):
            replaced = _replace(line=line, lang=lang, replacements=replacements)
            stripped = _strip(line=replaced, lang=lang)
            new_line = _whitespace(line=line, lang=lang) + stripped
        else:
            new_line = line
        new_lines.append(new_line)

    populated_template = '\n'.join(new_lines)

    return populated_template


def validate(template: str, lang: Language, replacements: Mapping[str, str]):
    missing_keys = []

    all_lines = _lines(template=template, lang=lang)
    all_stubbles = _flatten([_stubs(line=line, lang=lang) for line in all_lines])

    for stub in all_stubbles:
        if stub not in replacements.keys():
            missing_keys.append(stub)
    if missing_keys:
        raise AssertionError(f"Replacements missing keys: {missing_keys}")

    for key, val in replacements.items():
        if not isinstance(val, str):
            raise AssertionError("Replacements must contain only strings as values")



START_STUBBLE = "{{"
END_STUBBLE = "}}"


def _flatten(nested_list: List[List[Any]]):
    return list(itertools.chain.from_iterable(nested_list))


def _stub_indices(string: str, inclusive=True) -> Tuple[int, int]:
    if START_STUBBLE not in string or END_STUBBLE not in string:
        return 0, 0

    start_index = string.find(START_STUBBLE)
    end_index = string.find(END_STUBBLE)

    if inclusive:
        end_index += len(END_STUBBLE)
    else:
        start_index += len(START_STUBBLE)

    return start_index, end_index


def _strip(line: str, lang: Language) -> str:
    comment = comments[lang]
    stripped_line = line.lstrip()  # Remove leading whitespaces
    bare_line = stripped_line.lstrip(comment).strip()
    return bare_line


def _is_stubble_line(line: str, lang: Language) -> bool:
    stripped_line = _strip(line=line, lang=lang)

    if START_STUBBLE in stripped_line and END_STUBBLE in stripped_line:
        return True

    return False


def _lines(template: str, lang: Language) -> List[str]:
    all_lines = template.split('\n')
    stubble_lines = []

    for line in all_lines:
        if _is_stubble_line(line=line, lang=lang):
            stubble_lines.append(line)

    return stubble_lines


def _stubs(line: str, lang: Language) -> List[str]:
    return _stubble_internal(string=line, lang=lang, stubs=[])


def _stubble_internal(string: str, lang: Language, stubs: List[str]):
    new_list = copy(stubs)
    start, end = _stub_indices(string=string, inclusive=True)
    stub = string[start:end]
    if stub:
        no_brackets_stub = stub.removeprefix(START_STUBBLE).removesuffix(END_STUBBLE)
        no_whitespace_stub = no_brackets_stub.strip()
        new_list.append(no_whitespace_stub)
        new_string = string[end:]
        new_list = _stubble_internal(string=new_string, lang=lang, stubs=new_list)

    return new_list


def _whitespace(line: str, lang: Language) -> str:
    if not _is_stubble_line(line=line, lang=lang):
        raise ValueError("Line must be a valid stubble line.")

    comment = comments[lang]
    spaces, *rest = line.split(comment)
    return spaces



def _replace(line: str, lang: Language, replacements: Mapping[str, str]) -> str:
    stubs_in_line = _stubs(line=line, lang=lang)
    remaining_line = line
    for stub in stubs_in_line:
        start, end = _stub_indices(string=line, inclusive=True)
        remaining_line = remaining_line[:start] + replacements[stub] + remaining_line[end:]

    return remaining_line


