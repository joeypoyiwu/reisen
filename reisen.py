import click
from organize import commands as organize
from generate import commands as generate

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help']) 


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    logo = """
    +-----------------------------+
    |      Welcome to Reisen      |
    +-----------------------------+
    """
    click.echo(logo)
    click.echo('Run -h or --help for more information.\n')
    pass

cli.add_command(organize.organize)
cli.add_command(generate.generate)
