import click


@click.group()
@click.option('--template', required=True)
def main():
    pass


if __name__ == '__main__':
    main()
