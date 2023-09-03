import click
import os
from pathlib import Path
from stubbles.inputs import read_file_to_dict, language, list_files
from stubbles.templates import populate
from typing import List


@click.group(invoke_without_command=True)
@click.option('--template', type=click.Path(exists=True, dir_okay=True), required=True)
@click.option('--replacements', type=click.Path(exists=True, dir_okay=False), required=True)
@click.option('--output-dir', type=click.Path(dir_okay=True))
def cli(template, replacements, output_dir):
    if not output_dir:
        output_dir = Path('generated')
    if not isinstance(output_dir, Path):
        output_dir = Path(output_dir)
    if not isinstance(replacements, Path):
        replacements = Path(replacements)
    if not isinstance(template, Path):
        template = Path(template)

    main(
        template=template,
        replacements_file=replacements,
        output_dir=output_dir
    )


def main(template: Path, replacements_file: Path, output_dir: Path):
    replacements = read_file_to_dict(replacements_file)
    template_paths = list_files(template)
    populated_templates = []
    for template_path in template_paths:
        with open(template_path, 'r') as template_file:
            contents = template_file.read()
            lang = language(template_path.suffix)
            new_template = populate(template=contents, replacements=replacements, lang=lang)
            populated_templates.append(new_template)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for populated_template, template_path in zip(populated_templates, template_paths):
        name = template_path.name
        with open(output_dir / name, 'w') as template_file:
            template_file.write(new_template)


if __name__ == '__main__':
    cli()
