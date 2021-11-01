import click
from organize import commands as organize

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    logo = """
    +-----------------------------+
    |      Welcome to Reisen      |
    +-----------------------------+
    """
    click.echo(logo)
    pass

cli.add_command(organize.organize)
