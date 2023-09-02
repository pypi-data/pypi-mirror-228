from stubbles.types import Language, extensions


def language(extension: str) -> Language:
    for lang, exts in extensions.items():
        if extension in exts:
            return lang

    raise ValueError(f"Language not found for extension {extension}.")
