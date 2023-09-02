import click
from pathlib import Path
from stubbles.inputs import read_file_to_dict, language
from stubbles.templates import populate


@click.group()
@click.option('--template', type=click.Path(exists=True, dir_okay=False), required=True)
@click.option('--replacements', type=click.Path(exists=True, dir_okay=False), required=True)
@click.option('--output-dir', type=click.Path(dir_okay=True))
def cli(template, replacements, output_dir):
    if not output_dir:
        output_dir = Path('generated')

    main(
        template=template,
        replacements_file=replacements,
        output_dir=output_dir
    )


def main(template: Path, replacements_file: Path, output_dir: Path):
    replacements = read_file_to_dict(replacements_file)
    with open(template, 'r') as template_file:
        contents = template_file.read()
        lang = language(str(template))
        new_template = populate(template=contents, replacements=replacements, lang=lang)

    with open(output_dir / 'file.random', 'w') as file:
        file.write(new_template)


if __name__ == '__main__':
    cli()
