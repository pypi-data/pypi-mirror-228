import click
from docsdb.mongodb import mongodb
from docsdb.serve import serve
from docsdb.export import export


@click.group(help="DocsDB CLI")
def cli():
    pass


@click.group()
def generate():
    pass


generate.add_command(mongodb)

cli.add_command(generate)
cli.add_command(serve)
cli.add_command(export)


if __name__ == "__main__":
    cli()
